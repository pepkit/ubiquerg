""" Tests for system tools """

import pytest
from ubiquerg import is_command_callable
from veracitools import ExpectContext

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    ["cmd", "exp"], [("man", True), ("not-a-cmd", False), (None, ValueError)])
def test_command_callability_check(cmd, exp):
    """ Verify expected behavior of command callability checker. """
    with ExpectContext(exp, is_command_callable) as check_callable:
        check_callable(cmd)
