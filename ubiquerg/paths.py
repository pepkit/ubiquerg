""" Filesystem utility functions """

import os
import re
from .web import is_url

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["expandpath", "parse_registry_path"]


def expandpath(path):
    """
    Expand a filesystem path that may or may not contain user/env vars.

    :param str path: path to expand
    :return str: expanded version of input path
    """
    res = os.path.expandvars(os.path.expanduser(path))
    return res if is_url(path) else res.replace("//", "/")


def parse_registry_path(rpstring,
                        defaults=[
                            ("protocol", None),
                            ("namespace", None),
                            ("item", None),
                            ("subitem", None),
                            ("tag", None)]
                        ):
    """
    Parse a 'registry path' string into components.

    A registry path is a string that is kind of like a URL, providing a unique
    identifier for a particular asset, like
    protocol::namespace/item.subitem:tag. You can use the `defaults` argument to
    change the names of the entries in the return dict, and to provide defaults
    in case of missing values.

    :param str rpstring: string to parse
    :param list defaults: A list of 5 tuples with name of the 5 entries, and a
        default value in case it is missing (can be 'None')
    :return dict: dict with one element for each parsed entry in the path
    """

    # This commented regex is the same without protocol
    # ^(?:([0-9a-zA-Z_-]+)\/)?([0-9a-zA-Z_-]+)(?::([0-9a-zA-Z_.-]+))?$
    # regex = "^(?:([0-9a-zA-Z_-]+)(?:::|:\/\/))?(?:([0-9a-zA-Z_-]+)\/)?([0-9a-zA-Z_-]+)(?::([0-9a-zA-Z_.-]+))?$"
    regex = "^(?:([0-9a-zA-Z_-]+)(?:::|:\/\/))?(?:([0-9a-zA-Z_-]+)\/)?([0-9a-zA-Z_-]+)(?:\.([0-9a-zA-Z_-]+))?(?::([0-9a-zA-Z_.-]+))?$"
    # This regex matches strings like:
    # protocol://namespace/item:tag
    # or: protocol::namespace/item:tag
    # The names 'protocol', 'namespace', 'item', and 'tag' are generic and
    # you can use this function for whatever you like in this format... The
    # regex can handle any of these missing and will parse correctly into the
    # same element
    # For instance, you can leave the tag or protocol or both off:
    # ucsc://hg38/bowtie2_index
    # hg38/bowtie2_index
    # With no delimiters, it will match the item name:
    # bowtie2_index

    res = re.match(regex, rpstring)
    if not res:
        return None
    # position 0: parent namespace
    # position 1: namespace
    # position 2: primary name
    # position 3: tag
    captures = res.groups()
    parsed_identifier = {
        defaults[0][0]: captures[0] or defaults[0][1],
        defaults[1][0]: captures[1] or defaults[1][1],
        defaults[2][0]: captures[2] or defaults[2][1],
        defaults[3][0]: captures[3] or defaults[3][1],
        defaults[4][0]: captures[4] or defaults[4][1]
    }
    return parsed_identifier
