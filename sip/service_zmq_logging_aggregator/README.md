# Service: ZeroMQ Logging Aggregator

## Description

Service which aggregates logs using a ZeroMQ Subscriber socket. Aggregated
logs are written to stdout in the container.

The service also exposes a REST HTTP endpoint using Flask to provide a
health check.

Currently this is using a Flask development server and can be queried using:

```bash
curl http://localhost:5555/healthcheck
```

Finally the service exposes a Python Logging configuration server which allows
logging configuration files to be sent to the server at any point to update
the logging configuration. An example of how to send new configuration to this
can be found in `test/example_send_config.py`.

## Building the service as a docker image

The service is built by the Jenkins CI / CD service as **TODO(BM)**. It can 
also be built manually either using the docker build command or the provided
docker-compose file (`docker-compose.yml`) at the top of the SIP source tree. 

```bash
docker build -t sip/zla -f sip/service_zmq_logging_aggregator/Dockerfile .
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
python3 -m sip.service_zmq_logging_aggregator
```

or

```shell
docker run --rm -t -p 5555:5555 -p 9020:9020 --name zla sip/zla
```


Start one or more mock log publishers:

```shell
TODO
```
