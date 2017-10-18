# Service: ZeroMQ Logging Aggregator

## Description

Service which aggregates Python logging messages which have been sent using
ZeroMQ pub/sub sockets. Aggregated logs are written to stdout in the container.

The service also exposes a REST HTTP endpoint using
[Bottle](https://bottlepy.org/docs/dev/) and
[Bjoern](https://github.com/jonashaag/bjoern) to provide a health check API.
This can be used to check that the service is up and running before trying to
connect to it.

This can be queried using:

```bash
curl http://localhost:5555/health
```

and will return a JSON object with the fields:
 
- `module`, a string with value `zmq_logging_aggregator`
- `hostname`, the hostname which the logging aggregator is running
- `uptime` the length of time the logging aggregator has been running, in 
  seconds 

The service also exposes a Python Logging configuration server which allows
logging configuration files to be sent to the server to update the logging 
configuration. An example of how to send new configuration to this
can be found in `test/example_send_config.py`.

## Building the service as a docker image

The SIP Jenkins server builds this service as **TODO(BM)**. It can
also be built manually either using the docker build command or the provided
docker-compose file (`docker-compose.yml`) at the top of the SIP source tree.

```bash
docker build -t sip/zla sip/zmq_logging_aggregator
```

or

```bash
docker-compose build zla
```

## Usage

This service can either be run as a Docker Container or a Python application.
The application is configured using a JSON (or YAML) file which describes
the configuration of the output of the logger.

## Tests

The service can be tested by the provided mock log publisher application found
in the `/tests/mock_log_publisher.py` module.

*Running the test:*

Start the ZeroMQ Logging aggregator service:

```shell
python3 -m sip.zmq_logging_aggregator
```

or

```shell
docker run --rm -t -p 5555:5555 -p 9020:9020 --name zla sip/zla
```

Start one or more mock log publishers:

```shell
TODO
```

## Possible issues

1. Due to the Python GIL it may be possible for this code to fail to perform
   the task of receiving log messages at the same time as serving the 
   healthcheck and logging configuration server end-points. It may be possible
   to work around this using some form of asynchronous task queue or with 
   python multiprocessing.   
