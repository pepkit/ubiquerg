""" Tests for checksum """

import hashlib
import itertools
import pytest
from ubiquerg import checksum, size, filesize_to_str

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


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
    print(size_num)
    assert isinstance(filesize_to_str(size_num), str)
