# Service: ZeroMQ Logging Aggregator

## Quickstart

### Without containers

To run the service

```bash
python3 -m sip.zmq_logging_aggregator
```

To send test messages from a set of mock log publisher services

```bash
python3 -m sip.zmq_logging_aggreagtor.tests.example_start_publishers
```

### With containers using docker engine

Build docker images with:

```bash
docker-compose build zla
```

Run the service container

```bash
docker run --rm -t -p 5555:5555 -p 9020:9020 -p 9999:9999 --name zla sip/zla
```

To run the mock log publisher container
 
```bash
docker run --rm -t --name log_pub sip/mock_log_publisher
```

### With containers using Docker Swarm mode

```bash
docker service create ...
```



## Description

Service which aggregates Python logging messages received over ZeroMQ pub/sub
sockets. Aggregated logs are written to stdout. If running this service in a
container, logs can be viewed using the `docker logs`, or `docker service logs`
command, or attaching the local stdout to the container using the
`docker attach` command.

The service exposes three interfaces:

1. A ZMQ SUB socket which is bound to the default python logging TCP port, 9020
1. A REST HTTP health-check endpoint on port 5555 which can be queried on url
   `http://<host>:5555/healthcheck`
1. A standard Python Logging configuration server which listens on port 9999.


### ZMQ SUB socket

The services exposes a ZMQ SUB socket which is bound to the default python 
logging TCP port, 9020. Clients can publish messages to this port by connecting
a ZMQ PUB socket to the hostname of the logging service on this port.

When running this service on Docker Swarm, the service discovery provided by
the overlay network can be used to resolve the hostname of the service.


### Health Check API 

The service exposes a REST HTTP health-check endpoint using
[Bottle](https://bottlepy.org/docs/dev/) and
[Bjoern](https://github.com/jonashaag/bjoern) to provide a health check API.
This can be used to check that the service is up and running before trying to
connect to it.

This can be queried using:

```bash
curl http://localhost:5555/healthcheck
```

and will return a JSON object with the fields:

- `module`, a string with value `zmq_logging_aggregator`
- `hostname`, the hostname which the logging aggregator is running
- `uptime` the length of time the logging aggregator has been running, in
  second

### Logging Configuration Server

The service also exposes a Python Logging configuration server which allows
logging configuration files to be sent to the server to update the logging 
configuration. An example of how to send new configuration to this
can be found in `test/example_send_config.py`.

## Building the service Docker image

The SIP CI/CD Jenkins server builds this service as **TBD**. It can
also be built manually, either using the docker build command or the provided
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
python3 -m sip.zmq_logging_aggreagtor.tests.mock_log_publisher
```

or to start multiple publishers using python multiprocessing

```shell
python3 -m sip.zmq_logging_aggregator.tests.example_start_publishers
```


## Possible issues

1. Due to the Python GIL it may be possible for this code to fail to perform
   the task of receiving log messages at the same time as serving the 
   healthcheck and logging configuration server end-points. It may be possible
   to work around this using some form of asynchronous task queue or with 
   python multiprocessing.   
