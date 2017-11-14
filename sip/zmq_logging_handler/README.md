# Python logging ZeroMQ handler package

This package provides a Python logging handler which sends log messages
to a ZeroMQ PUB socket. This handler is intended to be used with the SIP
`zmq_logging_aggregator` service.

## Basic usage

```python
from sip.zmq_logging_handler.zmq_logging_handler import ZmqLogHandler
import logging

log = logging.getLogger(__name__)
log.addHandler(ZmqLogHandler(host='localhost'))
log.setLevel(logging.DEBUG)
log.debug('hello!')
```

## Configuration

The zmq logging handler constructor takes a `host` argument which is the host 
of the ZMQ logging aggregator subscriber socket on which to publish log 
messages. If running in Docker Swarm using an overlay network, 
this will be the name of the SIP ZeroMQ logging aggregator container 
(eg. `zla`). If not running in Docker Swarm this will be the IP address of the 
host running the ZMQ logging aggregator and some form of service discovery 
or static configuration will be required to set this.

When trying to connect to the logging aggregator, the handler will first 
attempt to query the healthcheck endpoint of the aggregator service and will 
therefore raise a `requests.exceptions.ConnectionError` exception if the
hostname is badly specified.
