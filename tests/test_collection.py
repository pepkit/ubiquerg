""" Tests for collection utilities """

import random
import string
import sys
import pytest
from ubiquerg.collection import *

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


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
def test_coll_like(arg, exp):
    """ Test arbiter of whether an object is collection-like. """
    assert exp == is_collection_like(arg)
