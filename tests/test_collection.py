""" Tests for collection utilities """

from collections import OrderedDict
import itertools
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


def combo_space(ks, items):
    """
    Create the Cartesian product of values sets, each bound to a key.

    :param Iterable[str] ks: subset of keys from the mapping items
    :param Mapping[str, Iterable[object]] items: bindings between key and
        collection of values
    :return itertools.product: Cartesian product of the values sets bound by
        the given subset of keys
    """
    return itertools.product(*[items[k] for k in ks])


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


def _generate_too_few_items(minsize, maxsize, pool):
    """
    Generate a "pool" of items of random size guaranteed less than given bound.

    :param int minsize: minimum pool size
    :param int maxsize: maximum pool size
    :param Iterable[object] pool: items from which to pull a subset for the
        returned pool
    :return Iterable[object]: subset of initial pool, constrained to be
        sufficiently small in accordance with given bounds
    :raise TypeError: if either size bound is not an integer
    :raise ValueError: if maxsize < minsize
    """
    print_bound = lambda: "[{}, {}]".format(minsize, maxsize)
    if not (isinstance(minsize, int) and isinstance(maxsize, int)):
        raise TypeError("Size bounds must be integers; got {}".
                        format(print_bound()))
    if maxsize < minsize:
        raise ValueError("Nonesense size bounds: {}".format(print_bound()))
    n = random.randint(minsize, maxsize)
    return n, random.sample(pool, max(n - 1, 0))


POWERSET_BOOL_KWARGSPACE = {
    p: [False, True] for p in
    get_default_parameters(powerset, lambda _, v: isinstance(v, bool))}
KWARGSPACE_POWERSET = {
    ks: combo_space(ks, POWERSET_BOOL_KWARGSPACE)
    for n in range(len(POWERSET_BOOL_KWARGSPACE) + 1)
    for ks in [tuple(c) for c in
               itertools.combinations(POWERSET_BOOL_KWARGSPACE.keys(), n)]}


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


@pytest.mark.parametrize("kwargs",
    [d for ks, vals_list in KWARGSPACE_POWERSET.items()
     for d in [dict(zip(ks, vs)) for vs in vals_list]])
def test_powerset_of_empty_pool(arbwrap, kwargs):
    """ Empty collection's powerset is always empty. """
    assert [] == powerset(arbwrap([]), **kwargs)


@pytest.mark.parametrize("include_full_pop", [False, True])
@pytest.mark.parametrize(
    ["min_items", "pool"],
    [_generate_too_few_items(
        2, 10, list(string.ascii_letters) + list(range(-10, 11)))
     for _ in range(5)])
def test_powerset_fewer_items_than_min(arbwrap, min_items, pool, include_full_pop):
    """ Minimum item count in excess of pool size results in empty powerset. """
    print("pool (n={}): {}".format(len(pool), pool))
    assert [] == powerset(arbwrap(pool), min_items=min_items,
                          include_full_pop=include_full_pop)


@pytest.mark.skip("not implemented")
@pytest.mark.parametrize(["pool", "kwargs", "expected"], [])
def test_powerset_legitimate_input(arbwrap, pool, kwargs, expected):
    """ Powerset behavior responds to arguments to its parameters """
    observed = powerset(arbwrap(pool), **kwargs)
    assert len(expected) == len(observed)
    assert expected == set(observed)


@pytest.mark.skip("not implemented")
def test_powerset_illegal_input(arbwrap):
    """ Invalid argument combination to powerset parameters is exceptional. """
    pass
