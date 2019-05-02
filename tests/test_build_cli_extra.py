""" Tests for rendering CLI options and arguments """

from collections import OrderedDict
import pytest
from ubiquerg import build_cli_extra

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(["optargs", "expected"], [
    ([("-X", None), ("--revert", 1), ("-O", "outfile"),
      ("--execute-locally", None), ("-I", ["file1", "file2"])],
     "-X --revert 1 -O outfile --execute-locally -I file1 file2")
])
def test_build_cli_extra(optargs, expected):
    """ Check that CLI optargs are rendered as expected. """
    observed = build_cli_extra(**OrderedDict(optargs))
    print("expected: {}".format(expected))
    print("observed: {}".format(observed))
    assert expected == observed
