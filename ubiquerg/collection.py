""" Tools for working with collections """

import sys
if sys.version_info < (3, 3):
    from collections import Iterable
else:
    from collections.abc import Iterable

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


__all__ = ["is_collection_like"]


def is_collection_like(c):
    """
    Determine whether an object is collection-like.

    :param object c: Object to test as collection
    :return bool: Whether the argument is a (non-string) collection
    """
    return isinstance(c, Iterable) and not isinstance(c, str)
