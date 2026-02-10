"""Validate what's available directly on the top-level import."""

from inspect import isclass, isfunction

import pytest

import ubiquerg


@pytest.mark.parametrize(
    ["obj_name", "typecheck"],
    [
        # cli_tools
        ("build_cli_extra", isfunction),
        ("convert_value", isfunction),
        ("query_yes_no", isfunction),
        ("VersionInHelpParser", isclass),
        # collection
        ("deep_update", isfunction),
        ("is_collection_like", isfunction),
        ("merge_dicts", isfunction),
        ("powerset", isfunction),
        ("uniqify", isfunction),
        # environment
        ("TmpEnv", isclass),
        # file_locking
        ("ensure_locked", isfunction),
        ("ensure_write_access", isfunction),
        ("locked_read_file", isfunction),
        ("make_all_lock_paths", isfunction),
        ("read_lock", isfunction),
        ("ThreeLocker", isclass),
        ("wait_for_locks", isfunction),
        ("write_lock", isfunction),
        # files
        ("checksum", isfunction),
        ("create_file_racefree", isfunction),
        ("create_lock", isfunction),
        ("filesize_to_str", isfunction),
        ("make_lock_path", isfunction),
        ("remove_lock", isfunction),
        ("size", isfunction),
        ("untar", isfunction),
        ("wait_for_lock", isfunction),
        # paths
        ("expandpath", isfunction),
        ("mkabs", isfunction),
        ("parse_registry_path", isfunction),
        ("parse_registry_path_strict", isfunction),
        # system
        ("is_command_callable", isfunction),
        ("is_writable", isfunction),
        # web
        ("is_url", isfunction),
    ],
)
def test_top_level_exports(obj_name, typecheck):
    """At package level, validate object availability and type."""
    try:
        obj = getattr(ubiquerg, obj_name)
    except AttributeError:
        pytest.fail("Unavailable on {}: {}".format(ubiquerg.__name__, obj_name))
    else:
        assert typecheck(obj)


@pytest.mark.parametrize("name", ["READ", "WRITE"])
def test_top_level_constants(name):
    """Constants used by downstream packages must be importable."""
    assert hasattr(ubiquerg, name)
    assert isinstance(getattr(ubiquerg, name), str)


def test_all_matches_exports():
    """__all__ must list every public name, and no extras."""
    actual = set(dir(ubiquerg)) - {n for n in dir(ubiquerg) if n.startswith("_")}
    declared = set(ubiquerg.__all__)
    missing = actual - declared
    # Filter out module names (submodule imports show up in dir())
    import types

    missing = {n for n in missing if not isinstance(getattr(ubiquerg, n), types.ModuleType)}
    extra = declared - actual
    assert not missing, f"In dir() but not __all__: {missing}"
    assert not extra, f"In __all__ but not importable: {extra}"
