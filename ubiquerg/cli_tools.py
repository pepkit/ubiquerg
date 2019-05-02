""" Functions for working with command-line interaction """

from .collection import is_collection_like

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["build_cli_extra"]


def build_cli_extra(optargs):
    """
    Render CLI options/args as text to add to base command.

    To specify a flag, map an option to None. Otherwise, map option short or
    long name to value(s). Values that are collection types will be rendered
    with single space between each. All non-string values are converted to
    string.

    :param Mapping | Iterable[(str, object)] optargs: values used as
        options/arguments
    :return str: text to add to base command, based on given opts/args
    :raise TypeError: if an option name isn't a string
    """

    def render(k, v):
        if not isinstance(k, str):
            raise TypeError(
                "Option name isn't a string: {} ({})".format(k, type(k)))
        if v is None:
            return k
        if is_collection_like(v):
            v = " ".join(map(str, v))
        return "{} {}".format(k, v)

    try:
        data_iter = optargs.items()
    except AttributeError:
        data_iter = optargs

    return " ".join(render(*kv) for kv in data_iter)
