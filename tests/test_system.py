""" Tests for system tools """

import os
import subprocess
import pytest
from ubiquerg import is_command_callable
from veracitools import ExpectContext

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

EXTENSIONS = [".py", ".rb", ".sh", ".java", ".jar", ".pl", ".o", ".R", ".r",
              ".cpp", ".c", ".hs", ".scala", ".class"]


def _mkfile(f):
    """ 'touch' a file. """
    with open(f, 'w'):
        print("Touch: {}".format(f))
    return f


@pytest.mark.parametrize(["cmd", "exp"], [
    ("man", True), ("not-a-cmd", False), (None, TypeError), ("", ValueError)])
def test_command_callability_check_basic(cmd, exp):
    """ Verify expected behavior of command callability checker. """
    with ExpectContext(exp, is_command_callable) as check_callable:
        check_callable(cmd)


@pytest.mark.parametrize(
    "relpath",
    ["subdir", os.path.join("subA", "subB")] +
    ["testfile" + ext for ext in EXTENSIONS])
def test_missing_path_isnt_callable(tmpdir, relpath):
    """ A filepath that doesn't exist (and isn't on PATH) isn't callable. """
    p = os.path.join(tmpdir.strpath, relpath)
    assert not os.path.exists(p)
    assert not is_command_callable(p)


@pytest.mark.parametrize(
    "get_arg", [lambda d: d, lambda d: os.path.join(d, "subdir")])
def test_extant_folder_isnt_callable(tmpdir, get_arg):
    """ A directory path can't be callable. """
    p = get_arg(tmpdir.strpath)
    print("p: {}".format(p))
    if not os.path.exists(p):
        os.makedirs(p)
    assert os.path.exists(p)
    assert not is_command_callable(p)


@pytest.mark.parametrize("filepath", [
    lambda d: os.path.join(d, "testfile" + ext) for ext in EXTENSIONS])
@pytest.mark.parametrize(["setup", "exp_exe"], [
    (lambda _: None, False),
    (lambda f: subprocess.check_call(["chmod", "+x", f]), True)])
def test_extant_file_requires_exec_for_callability(tmpdir, filepath, setup, exp_exe):
    """ Filepath is callable iff it has exec bit. """
    f = filepath(tmpdir.strpath)
    assert not os.path.exists(f)
    _mkfile(f)
    assert os.path.isfile(f)
    setup(f)
    assert os.access(f, os.X_OK) is exp_exe
    assert is_command_callable(f) is exp_exe
