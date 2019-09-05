# Changelog

## [0.4.9] - unreleased
### Added
- add `--version` argument in `VersionInHelpParser`

## [0.4.8] - 2019-08-27
### Added
- `parse_registry_path` function.

## [0.4.7] - 2019-08-09
### Fixed
- `is_writable` function; [Issue 16](https://github.com/pepkit/ubiquerg/issues/16)

## [0.4.6] - 2019-08-08
### Added
- file/directory size checker
- `is_writable` function

## [0.4.5] - 2019-07-01
### Changed
- If argument to callability checker is a file, require executability; if it's a folder, it's not callable.
### Fixed
- Populate intended field in error message for bad argument to callability checker.

## [0.4.4] - 2019-06-20
### Added
- Command callability checker

## [0.4.3] - 2019-06-06
### Changed
- To avoid implicitly wrapping `input()` in `eval`, never use `2to3`.

## [0.4.2] - 2019-06-06
### Fixed
- More robust handling of terminal interaction in `query_yes_no`

## [0.4] - 2019-05-31
### Added
- `checksum`, using md5
- `query_yes_no` to facilitate binary user terminal interaction

## [0.3] - 2019-05-29
### Added
- `TmpEnv`: environment variable context manager

## [0.2.1] - 2019-05-16
### Changed
- Use `is_url` to determine slash behavior in `expandpath`

## [0.2] - 2019-05-16
### Added
- `is_url`

## [0.1] - 2019-05-08
### Changed
- Remove `ExpectContext`; see [`veracitools`](https://github.com/pepkit/veracitools)

## [0.0.5.1] - 2019-05-08
### Fixed
- Control exports to fix a docs build issue; see [Issue 2](https://github.com/pepkit/ubiquerg/issues/2)

## [0.0.5] - 2019-05-08
### Added
- `expandpath` utility for dealing with user and environment variables in paths

## [0.0.4] - 2019-05-03
### Added
- `ExpectContext` for uniform test execution, regardless of whether expectation is an ordinary object or an exception
### Changed
- When minimum item count exceeds pool size and/or the "pool" of items is empty, `powerset` returns an empty collection rather than a collection with a single empty element.

## [0.0.3] - 2019-05-02
### Added
- CLI optarg string builder (`build_cli_extra`)
- `powerset` (all subsets of a collection)

## [0.0.2] - 2019-05-01
## Changed
- Restrict offerings to most generic functionality.

## [0.0.1] - 2019-04-30
- First release version
