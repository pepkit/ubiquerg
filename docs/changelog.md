# Changelog

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
