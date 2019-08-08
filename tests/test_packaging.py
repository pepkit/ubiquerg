""" Validate what's available directly on the top-level import. """

import pytest
from inspect import isclass, isfunction

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    ["obj_name", "typecheck"],
    [("build_cli_extra", isfunction), ("checksum", isfunction), ("size", isfunction),
     ("expandpath", isfunction), ("is_collection_like", isfunction),
     ("is_command_callable", isfunction), ("is_url", isfunction),
     ("powerset", isfunction), ("query_yes_no", isfunction),
     ("TmpEnv", isclass)])
def test_top_level_exports(obj_name, typecheck):
    """ At package level, validate object availability and type. """
    import ubiquerg
    try:
        obj = getattr(ubiquerg, obj_name)
    except AttributeError:
        pytest.fail("Unavailable on {}: {}".format(ubiquerg.__name__, obj_name))
    else:
        assert typecheck(obj)
