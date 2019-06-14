""" System utility functions """

import os
__author__ = "Databio Lab"
__email__ = "nathan@code.databio.org"

__all__ = ["is_command_callable"]



def is_command_callable(self, command, name=""):
    """
    Check if command can be called.

    :param str command: actual command to call
    :param str name: nickname/alias by which to reference the command
    :return bool: whether given command's call succeeded
    """
    name = name or command
    # Use `command` to see if command is callable, store exit code
    code = os.system(
        "command -v {0} >/dev/null 2>&1 || {{ exit 1; }}".format(command))
    if code != 0:
        alias_value = " ('{}') ".format(name) if name else " "
        _LOGGER.debug("Command '{0}' is not callable: {1}".
                      format(alias_value, command))
    return not bool(code)
