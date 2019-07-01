""" System utility functions """

import os

__author__ = "Databio Lab"
__email__ = "nathan@code.databio.org"

__all__ = ["is_command_callable"]


def is_command_callable(cmd):
    """
    Check if command can be called.

    :param str cmd: actual command to check for callability
    :return bool: whether given command's call succeeded
    :raise TypeError: if the alleged command isn't a string
    :raise ValueError: if the alleged command is empty
    """
    if not isinstance(cmd, str):
        raise TypeError("Alleged command isn't a string: {} ({})")
    if not cmd:
        raise ValueError("Empty command to check for callability")
    if os.path.isdir(cmd) or (os.path.isfile(cmd) and not os.access(cmd, os.X_OK)):
        return False
    # Use `command` to see if command is callable, and rule on exit code.
    check = "command -v {0} >/dev/null 2>&1 || {{ exit 1; }}".format(cmd)
    return not bool(os.system(check))
