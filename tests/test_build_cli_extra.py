""" Tests for rendering CLI options and arguments """

from collections import OrderedDict
import pytest
from ubiquerg import build_cli_extra, powerset

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


def pytest_generate_tests(metafunc):
    """ Test case generation and parameterization for this module """
    if "ordwrap" in metafunc.fixturenames:
        metafunc.parametrize("ordwrap", [tuple, OrderedDict])


@pytest.mark.parametrize(["optargs", "expected"], [
    ([("-X", None), ("--revert", 1), ("-O", "outfile"),
      ("--execute-locally", None), ("-I", ["file1", "file2"])],
     "-X --revert 1 -O outfile --execute-locally -I file1 file2")
])
def test_build_cli_extra(optargs, expected, ordwrap):
    """ Check that CLI optargs are rendered as expected. """
    observed = build_cli_extra(ordwrap(optargs))
    print("expected: {}".format(expected))
    print("observed: {}".format(observed))
    assert expected == observed


@pytest.mark.parametrize(
    "optargs", powerset([(None, "a"), (1, "one")], nonempty=True))
def test_illegal_cli_extra_input_is_exceptional(optargs, ordwrap):
    """ Non-string keys are illegal and cause a TypeError. """
    with pytest.raises(TypeError):
        build_cli_extra(ordwrap(optargs))
