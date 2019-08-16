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


def parse_registry_path(rpstring, names=["protocol", "namespace", "item", "subitem" "tag"]):
    """
    Parse a 'registry path' string into components.

    A registry path is a string that is kind of like a URL, providing a unique
    identifier for a particular asset, like protocol::namespace/item.subitem:tag.

    :param str rpstring: string to parse
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
        names[0]: captures[0],
        names[1]: captures[1],
        names[2]: captures[2],
        names[3]: captures[3],
        names[4]: captures[4]
    }
    return parsed_identifier
