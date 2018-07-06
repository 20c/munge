
# Change log for munge

## [Unreleased]
### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security


## [0.6.0]
### Fixed
- log on click Context referencing non-existant `cls` property

### Changed
- decrease PyYAML requirement to >=3.10


## [0.5.0]
### Added
- option_list to Context
- log to Context
- config search path includes ~/.$APP_NAME

### Changed
- empty meta returns empty dict instead of None


## [0.4.0]
### Added
- py3 support

### Fixed
- set click.Context.home when config is found


## [0.3.0]
### Fixed
- version bump for proper semantic versioning


## [0.2.1]

### Added
- CHANGELOG!
- allow changing config_name
- try_read
- config.meta
- config.copy()
- click.Context

### Removed
- unused get_type, Endpoint

