"""Package exports

Version is defined in pyproject.toml. To get it at runtime:
    from importlib.metadata import version
    version("ubiquerg")
"""

from .cli_tools import (
    VersionInHelpParser,
    build_cli_extra,
    convert_value,
    query_yes_no,
)
from .collection import deep_update, is_collection_like, merge_dicts, powerset, uniqify
from .environment import TmpEnv
from .file_locking import (
    READ,
    WRITE,
    ThreeLocker,
    ensure_locked,
    ensure_write_access,
    locked_read_file,
    make_all_lock_paths,
    read_lock,
    wait_for_locks,
    write_lock,
)
from .files import (
    checksum,
    create_file_racefree,
    create_lock,
    filesize_to_str,
    make_lock_path,
    remove_lock,
    size,
    untar,
    wait_for_lock,
)
from .paths import expandpath, mkabs, parse_registry_path, parse_registry_path_strict
from .system import is_command_callable, is_writable
from .web import is_url

__all__ = [
    "build_cli_extra",
    "checksum",
    "convert_value",
    "create_file_racefree",
    "create_lock",
    "deep_update",
    "ensure_locked",
    "ensure_write_access",
    "expandpath",
    "filesize_to_str",
    "is_collection_like",
    "is_command_callable",
    "is_url",
    "is_writable",
    "locked_read_file",
    "make_all_lock_paths",
    "make_lock_path",
    "merge_dicts",
    "mkabs",
    "parse_registry_path",
    "parse_registry_path_strict",
    "powerset",
    "query_yes_no",
    "READ",
    "read_lock",
    "remove_lock",
    "size",
    "ThreeLocker",
    "TmpEnv",
    "uniqify",
    "untar",
    "VersionInHelpParser",
    "wait_for_lock",
    "wait_for_locks",
    "WRITE",
    "write_lock",
]
