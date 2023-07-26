
# Changelog

<!-- ## [Unreleased]

### Added
- New feature X
- New feature Y

### Changed
- Improved performance of feature A
- Updated dependency B to version 2.0

### Fixed
- Bug in feature C that caused crashes -->

## [0.2.0] - 2021-08-01

### Added
- Session Id to session object, this is the unique id for the user session
- Timeout controller and handlers: now you can set a timeout for the user to respond to a message and handle the timeout event


### Changed
- **lead** parameter for **session** parameter on functions on_event and on_command, lead is now a property of session


### Fixed
- None