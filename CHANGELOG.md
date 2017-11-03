# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security


## [0.3.0] - 2017-10-xx
### Added
- Standalone ZeroMQ logging service. This can be run as a binary or as a docker
  container. This can be found in the `zmq_logging_aggregator` folder.
### Changed
- Updated modules throughout SIP to make use of standard Python Logging. 
  Removed use of a global Python logging object defined in 
  `sip/common/logging_api.py`. 
### Removed
- Logging code in the `sip.common` module which is now deprecated:
  - `sip/common/logging_aggregator.py`
  - `sip/common/logging_api.py`
  - `sip/common/logging_handlers.py`
  - `sip/common/logging_server.py`
### Fixed
- Updated top level README.md file. This is still out of date and will be 
  updated as part of a future documentation update activity.
- Various PEP8 and PyLint issues.
### Deprecated
- `sip_run.py` has been marked deprecated.  

## [0.2.2] - 2017-10-02
### Changed
- Unit test coverage filter in the Jenkins file to omit files which do not need
  testing.
- Jenkins' 'Analysis' stage no longer affects the build status, ending our
  perpetual state of unstableness.
### Fixed
- Unit test naming conventions. All unit tests files should be prefixed with
  with `test_`, examples with `example_`, and test mock objects with `mock_`. 
  For more information see 
  [SIP: Unit test naming convensions](https://confluence.ska-sdp.org/display/WBS/SIP%3A+Unit+test+naming+conventions).
- Various PEP-8 and PyLint errors in unit tests.
- The 'success' post-build status crashed the Jenkins build due to typo's in the
  commands.
### Removed
- Python modules in requirements.txt related to non core SIP functions. These
  these should be moved into their own module but for now are simply disabled.
- A number of broken unit tests have been marked as skipped and their file
  names prefixed with `disabled_`. 

 
## [0.2.1] - 2017-09-12
### Fixed
- Jenkinsfile to work around a bug in the code where hanging docker services
  results in the Jenkins server crashing.

## [0.2.0] - 2017-09-08
### Added
- Changelog file. This will be used from now on to keep a top level summary of 
  changes. Versions will also be tagged as GitHub releases.
### Changed
- Updated to version 0.2.0.
### Fixed
- Various pep8 / pylint errors problems in `setup.py`
