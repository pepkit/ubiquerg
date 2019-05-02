""" Functions for working with command-line interaction """

from .collection import is_collection_like

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def build_cli_extra(**kwargs):
    """
    Render CLI options/args as text to add to base command.

    To specify a flag, map an option to None. Otherwise, map option short or
    long name to value(s). Values that are collection types will be rendered
    with single space between each. All non-string values are converted to
    string.

    :return str: text to add to base command, based on given opts/args
    """

    def render(k, v):
        if v is None:
            return k
        if is_collection_like(v):
            return " ".join(map(str, v))
        return str(v)

    return " ".join(render(*kv) for kv in kwargs.items())
