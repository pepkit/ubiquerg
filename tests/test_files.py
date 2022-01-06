""" Tests for checksum """

import hashlib
import os
import itertools
import pytest

from tempfile import mkdtemp
from ubiquerg import checksum, size, filesize_to_str, make_lock_path, \
    create_file_racefree, wait_for_lock, create_lock, remove_lock


def pytest_generate_tests(metafunc):
    """ Dynamic test case generation/parameterization for this module. """
    if "size1" in metafunc.fixturenames and "size2" in metafunc.fixturenames:
        metafunc.parametrize(
            ["size1", "size2"], itertools.product([1, 4], [2, 8]))
    if "lines" in metafunc.fixturenames:
        metafunc.parametrize("lines", [[], ["line1"], ["line1", "line2"]])


def test_checksum(size1, size2, lines, tmpdir):
    """ Checksum result matches expectation and is blocksize-agnostic """
    fp = tmpdir.join("temp-data.txt").strpath
    data = "\n".join(lines)
    with open(fp, 'w') as f:
        f.write(data)
    exp = hashlib.new("md5", data.encode("utf-8")).hexdigest()
    res1 = checksum(fp, size1)
    res2 = checksum(fp, size2)
    assert exp == res1
    assert res1 == res2
    assert res2 == exp


def test_size_returns_str(lines, tmpdir):
    """ Size returns a string and works with both files and directories """
    fp = tmpdir.join("temp-data.txt").strpath
    data = "\n".join(lines)
    with open(fp, 'w') as f:
        f.write(data)
    assert isinstance(size(fp), str)
    assert isinstance(size(tmpdir.strpath), str)


def test_size_returns_int(lines, tmpdir):
    fp = tmpdir.join("temp-data.txt").strpath
    fp_larger = tmpdir.join("temp-data.txt").strpath
    data = "\n".join(lines)
    with open(fp, 'w') as f:
        f.write(data)
    with open(fp_larger, 'w') as f1:
        f1.write(data * 100)
    assert isinstance(size(tmpdir.strpath, False), int)
    assert isinstance(size(fp, False), int)
    assert size(fp, size_str=False) <= size(fp, size_str=False)


def test_nonexistent_path(tmpdir):
    """ Nonexistent path to checksum is erroneous. """
    with pytest.raises(IOError):
        checksum(tmpdir.join("does-not-exist.txt").strpath)


@pytest.mark.parametrize("size_num", list(range(0, 10)) + [i/3 for i in range(0, 10)])
def test_filesize_to_str_int(size_num):
    """ Works with int and returns str """
    assert isinstance(filesize_to_str(size_num), str)


@pytest.mark.parametrize("obj", ["test", [], tuple()])
def test_filesize_to_str_other(obj):
    """ Returns the original object if it's not an int or float and warns """
    with pytest.warns(UserWarning):
        assert filesize_to_str(obj) == obj


class TestLocking:
    @pytest.mark.parametrize("pth", ["test", "", "/home/me/test.yaml", "1"])
    def test_lock_path_creation_string(self, pth):
        assert "lock." in make_lock_path(pth)

    @pytest.mark.parametrize("pth", [["test", ""], ["/home/me/test.yaml", "1"]])
    def test_lock_path_creation_multi(self, pth):
        assert len(make_lock_path(pth)) == len(pth)

    @pytest.mark.parametrize("fn", ["a.yaml", "a.txt"])
    def test_racefree_file_creation_basic(self, fn):
        fp = os.path.join(mkdtemp(), fn)
        create_file_racefree(fp)
        assert os.path.exists(fp)

    @pytest.mark.parametrize("fn", ["a.yaml", "a.txt"])
    def test_racefree_file_creation_errors(self, fn):
        fp = os.path.join(mkdtemp(), fn)
        fh = os.open(fp, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fh)
        with pytest.raises(OSError):
            create_file_racefree(fp)

    @pytest.mark.parametrize("lp", ["a.yaml", "a.txt"])
    def test_waiting_for_lock_basic(self, lp):
        wait_for_lock(lp)

    @pytest.mark.parametrize("ln", ["a.yaml", "a.txt"])
    def test_waiting_for_lock_exists(self, ln):
        lp = os.path.join(mkdtemp(), ln)
        fh = os.open(lp, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fh)
        with pytest.raises(RuntimeError):
            wait_for_lock(lp, 0.01)

    @pytest.mark.parametrize("fn", ["a.yaml", "a.txt"])
    def test_lock_file_creation_and_removal(self, fn):
        td = mkdtemp()
        create_lock(os.path.join(td, fn))
        locks_list = \
            [os.path.join(td, f) for f in os.listdir(td) if f.startswith("lock.")]
        assert len(locks_list) == 1
        remove_lock(os.path.join(td, fn))
        locks_list = \
            [os.path.join(td, f) for f in os.listdir(td) if f.startswith("lock.")]
        assert len(locks_list) == 0
