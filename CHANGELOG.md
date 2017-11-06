# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
 - Master controller can now run containerised (as well as non-containerised).
  - Made `sip` overlay network attachable
	- Master controller attaches to `sip` overlay network when running
    containerised
  - Removed all hard references to `localhost`, all communications now happen
    through hostnames on the `sip` overlay or the master's actual hostname
 - Replaced global container/Dockerfile with docker-compose based set of
   task-specific, hierarchichal containers in `sip/containers`.
 - Docker slaves now run on the image specified in sip/etc/slave\_map.json
   instead of defaulting to the 'sip' image.
 - Docker image labels are now taken into account when running through the 
   `SIP_IMAGE_LABEL` environment variable, both when building and when running.
   The default value is `latest`.

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
  names prefixed with `DISABLED`. 

 
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
