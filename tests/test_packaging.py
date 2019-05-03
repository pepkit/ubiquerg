""" Validate what's available directly on the top-level import. """

import pytest

__author__ = "Vince Reuter"
__email__ = "vreuter@virginia.edu"


@pytest.mark.parametrize(
    ["obj_name", "typecheck"],
    [("build_cli_extra", callable), ("is_collection_like", callable),
     ("powerset", callable),
     ("ExpectContext", lambda obj: isinstance(obj, type))])
def test_top_level_exports(obj_name, typecheck):
    """ At package level, validate object availability and type. """
    import ubiquerg
    try:
        obj = getattr(ubiquerg, obj_name)
    except AttributeError:
        pytest.fail("Unavailable on {}: {}".format(ubiquerg.__name__, obj_name))
    else:
        assert typecheck(obj)
