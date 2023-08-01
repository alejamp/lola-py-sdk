
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
## [0.3.0] - 2023-08-1

### Added
- New support for debugging. Now you can start lola SDK with ``` lola.listan(debug=True) ``` 
this will print all the debug messages that are sent and received from the server.


## [0.2.2] - 2023-07-15

### Changed
- Add easy way to set timeout with less code: 
```python 
ctx.set_timeout(5, '5_seconds_without_message')
```


## [0.2.0] - 2023-07-10

### Added
- Session Id to session object, this is the unique id for the user session
- Timeout controller and handlers: now you can set a timeout for the user to respond to a message and handle the timeout event


### Changed
- **lead** parameter for **session** parameter on functions on_event and on_command, lead is now a property of session


### Fixed
- None