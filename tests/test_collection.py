""" Tests for collection utilities """

from collections import OrderedDict
import sys
if sys.version_info.major < 3:
    from inspect import getargspec as get_fun_sig
else:
    from inspect import getfullargspec as get_fun_sig
import random
import string
import sys
import pytest
from ubiquerg.collection import *

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def get_default_parameters(func, pred=None):
    """
    For given function, get mapping from parameter name to default value.

    :param callable func: the function to inspect
    :param func(object, object) -> bool pred: how to determine whether the
        parameter should be included, based on name and default value
    :return OrderedDict[str, object]]: mapping from parameter name to default value
    """
    if not callable(func):
        raise TypeError("Not a callable: {} ({})".format(func.__name__, type(func)))
    spec = get_fun_sig(func)
    par_arg_pairs = zip(spec.args[(len(spec.args) - len(spec.defaults)):],
                        spec.defaults)
    return OrderedDict(
        par_arg_pairs if pred is None else
        [(p, a) for p, a in par_arg_pairs if pred(p, a)])


POWERSET_BOOL_KWARGSPACE = {
    p: [False, True] for p in
    get_default_parameters(powerset, lambda _, v: isinstance(v, bool))}


def pytest_generate_tests(metafunc):
    """ Test case generation and parameterization for this module """
    if "arbwrap" in metafunc.fixturenames:
        metafunc.parametrize("arbwrap", [list, tuple, set, iter])


def randcoll(pool, dt):
    """
    Generate random collection of 1-10 elements.

    :param Iterable pool: elements from which to choose
    :param type dt: type of collection to create
    :return Iterable[object]: collection of randomly generated elements
    """
    valid_types = [tuple, list, set, dict]
    if dt not in valid_types:
        raise TypeError("{} is an invalid type; choose from {}".
                        format(str(dt), ", ".join(str(t) for t in valid_types)))
    rs = [random.choice(pool) for _ in range(random.randint(1, 10))]
    return dict(enumerate(rs)) if dt == dict else rs


@pytest.mark.parametrize(
    ["arg", "exp"],
    [(random.randint(-sys.maxsize - 1, sys.maxsize), False),
     (random.random(), False),
     (random.choice(string.ascii_letters), False),
     ([], True), (set(), True), (dict(), True), (tuple(), True),
     (randcoll(string.ascii_letters, list), True),
     (randcoll(string.ascii_letters, dict), True),
     (randcoll([int(d) for d in string.digits], tuple), True),
     (randcoll([int(d) for d in string.digits], set), True),
     ("", False), ("abc", False)]
)
def test_is_collection_like(arg, exp):
    """ Test arbiter of whether an object is collection-like. """
    assert exp == is_collection_like(arg)


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize("kwargs", [])
def test_powerset_of_empty_pool(arbwrap, kwargs):
    assert [] == powerset(arbwrap([]), **kwargs)


@pytest.mark.skip("not implemented")
def test_powerset_fewer_items_than_min(pool, arbwrap, kwargs):
    assert [] == powerset(arbwrap(pool), **kwargs)


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["pool", "kwargs", "expected"], [])
def test_powerset_legitimate_input(arbwrap, pool, kwargs, expected):
    observed = powerset(arbwrap(pool), **kwargs)
    assert len(expected) == len(observed)
    assert expected == set(observed)


@pytest.mark.skip("not implemented")
def test_powerset_illegal_input(arbwrap):
    pass
