""" Functions for working with command-line interaction """

from .collection import is_collection_like
from argparse import ArgumentParser, _SubParsersAction, _HelpAction
import sys

__classes__ = ["VersionInHelpParser"]
__all__ = __classes__ + ["build_cli_extra", "query_yes_no"]


class VersionInHelpParser(ArgumentParser):

    def __init__(self, version=None, **kwargs):
        """ Overwrites the inherited init. Saves the version as an object
        attribute for further use. """
        super(VersionInHelpParser, self).__init__(**kwargs)
        self.version = version
        if self.version is not None:
            self.add_argument('--version', action='version',
                              version='%(prog)s {}'.format(self.version))

    def format_help(self):
        """ Add version information to help text. """
        help_string = "version: {}\n".format(str(self.version)) \
            if self.version is not None else ""
        return help_string + super(VersionInHelpParser, self).format_help()

    def subparsers(self):
        """
        Get the subparser associated with a parser.

        :return argparse._SubparsersAction: action defining the subparsers
        """
        subs = [a for a in self._actions if isinstance(a, _SubParsersAction)]
        if len(subs) != 1:
            raise ValueError(
                "Expected exactly 1 subparser, got {}".format(len(subs)))
        return subs[0]

    def subcommands(self):
        """
        Get subcommands defined by a parser.

        :return list[str]: subcommands defined within this parser
        """
        return list(self.subparsers().choices.keys())

    def dests_by_subparser(self, subcommand=None):
        """
        Get argument dests by subcommand from a parser.

        :param str subcommand: subcommand to get dests for
        :return dict: dests by subcommand
        """
        if subcommand is not None and subcommand not in self.subcommands():
            raise ValueError("'{}' not found in this parser commands: {}".
                             format(subcommand, str(self.subcommands())))
        subs = self.subparsers().choices if subcommand is None \
            else {subcommand: self.subparsers().choices[subcommand]}
        dests = {}
        for subcmd, sub in subs.items():
            dest_list = []
            for action in sub._actions:
                if isinstance(action, _HelpAction):
                    continue
                if hasattr(action, "dest"):
                    dest_list.append(action.dest)
            dests[subcmd] = dest_list
        return dests


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

    :param str question: a string that is presented to the user.
    :param str default: the presumed answer if the user just hits <Enter>.
    :return bool: True for "yes" or False for "no"
    """
    def parse(ans):
        return {"yes": True, "y": True, "ye": True,
                "no": False, "n": False}[ans.lower()]
    try:
        prompt = {None: "[y/n]", "yes": "[Y/n]",
                  "no": "[y/N]"}[None if default is None else default.lower()]
    except (AttributeError, KeyError):
        raise ValueError("invalid default answer: {}".format(default))
    msg = "{q} {p} ".format(q=question, p=prompt)
    while True:
        sys.stdout.write(msg)
        try:
            return parse(_read_from_user() or default)
        except KeyError:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def _read_from_user():
    import sys
    if sys.version_info.major < 3:
        from __builtin__ import raw_input
        return raw_input()
    return input()
