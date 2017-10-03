[![Documentation Status](https://readthedocs.org/projects/integration-prototype/badge/?version=latest)](http://integration-prototype.readthedocs.io/en/latest/?badge=latest)
[![Build Status](http://128.232.224.174/buildStatus/icon?job=sip/master)](http://128.232.224.174/job/sip/job/master/)
[![GitHub (pre-)release](https://img.shields.io/github/release/SKA-ScienceDataProcessor/integration-prototype/all.svg)](https://github.com/SKA-ScienceDataProcessor/integration-prototype/releases)

# SDP Integration Prototype

## Introduction

The SDP Integration prototype is a project to develop a lightweight prototype 
of the major components of the SDP system. The focus of this prototype is to:

- provide verification, testing and analysis of the SDP architecture,
- test external (to other SKA components) and internal (to other SDP 
  components) software interfaces,
- provide limited tests of horizontal scaling on representative SDP hardware 
  prototype (AlaSKA performance prototype platform (P3))

## The SIP code

SIP consists of two main categories of components:

1. A set of services which for control, monitoring and other persistent
   services required to be running to support a functional SDP.
2. A number of capability tasks which are started using the control
   service(s) and perform various tasks mocking SDP processing or data ingest 
   tasks.

Currently all SIP code resides in the `/sip` folder which is a single python
project with sub-module for the Master Controller, Slave controller,
Processor software, tasks, and common utility functions. This folder structure
is under active review and is likely to change in the short term (~weeks).


## Requirements

The SIP code required Python 3.5+ and has a number of dependencies which are
listed in the `requirements.txt` file in the top level of the build tree.

In addition to these Python requirements, in order to run the SIP code,
Docker must be installed and configured in Swarm mode.

Instructions for this can be found in the source documentation at
TODO(BM) Link to readthedocs (needs updating...)

Please also refer to the SIP confluence pages for more information.

A test apache spark pipeline can also be started by the SIP code if a local
spark cluster is installed with a HTTP endpoint on the node which is running 
the Master Controller.

## Running SIP

TODO(BM) Create a branch to update this doc. Brief doc here with additional 
details in the sphinx? 





