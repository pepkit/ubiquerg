""" Functions for working with command-line interaction """

from .collection import is_collection_like
import sys

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"

__all__ = ["build_cli_extra", "query_yes_no"]


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


def query_yes_no(question, default="no"):
    """
    Ask a yes/no question via raw_input() and return their answer.
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).
    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {
        "yes": True, "y": True, "ye": True,
        "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
