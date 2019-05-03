""" Tests for ExpectContext """

import pytest
from ubiquerg import ExpectContext

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def atterr(*args, **kwargs):
    raise AttributeError()


def ioerr(*args, **kwargs):
    raise IOError()


def keyerr(*args, **kwargs):
    raise KeyError()


def typerr(*args, **kwargs):
    raise TypeError()


FUN_BY_ERR = {IOError: ioerr, TypeError: typerr,
              KeyError: keyerr, AttributeError: atterr}


@pytest.mark.parametrize(
    ["err", "fun", "expect_success"],
    [t for err, fun in FUN_BY_ERR.items()
     for t in [(err, fun, True)] +
     [(err, unfun, False) for unfun in
      [f for e, f in FUN_BY_ERR.items() if e != err]]])
@pytest.mark.parametrize("args", [tuple(), ("a", ), ("b", 1)])
@pytest.mark.parametrize("kwargs", [{}, {"a": 0}, {"a": 1, "b": [1, 2]}])
def test_exp_ctx_exceptional_result(err, fun, expect_success, args, kwargs):
    """ The expectation context correctly handles exceptional expectation. """
    try:
        with ExpectContext(expected=err, test_func=fun) as ctx:
            ctx(*args, **kwargs)
    except AssertionError as e:
        if expect_success:
            # Wrong failure type
            pytest.fail(str(e))
    except Exception as e:
        if expect_success:
            pytest.fail("Expected to catch a {} but hit {}".
                        format(type(err), type(e)))


@pytest.mark.parametrize(
    ["exp_res", "fun", "expect_success"],
    [(2, lambda *args, **kwargs: 2, True),
     (-1, lambda *args, **kwargs: 0, False)])
@pytest.mark.parametrize("args", [tuple(), ("a", ), ("b", 1)])
@pytest.mark.parametrize("kwargs", [{}, {"a": 0}, {"a": 1, "b": [1, 2]}])
def test_exp_ctx_ordinary_result(exp_res, fun, expect_success, args, kwargs):
    """ The expectation context correctly handles ordinary expectation. """
    try:
        with ExpectContext(expected=exp_res, test_func=fun) as ctx:
            res = ctx(*args, **kwargs)
    except AssertionError as e:
        if expect_success:
            pytest.fail("Expected success but assertion failed: {}".format(e))
    else:
        if not expect_success:
            pytest.fail("Unexpected function execution success (feigned "
                        "expectation {} and got {})".format(exp_res, res))
