#
# docker build -t sip/zlp sip/zmq_logging_aggregator/tests/mock_log_publisher
#
# Run with (assumes the ZeroMQ Logging aggreagtor container has already
# started):
#   docker run --rm -t --name zlp --network container:zla sip/zlp <name>
#
# Debug with:
#   docker run --rm -it --entrypoint=/bin/sh sip/zlp
#

FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

COPY requirements.txt /app/requirements.txt

# Note
# - libstdc++ is installed as a separate step as this is needed for
#   pyzmq and should not be deleted when removing build dependencies.
# - curl is needed for the healthcheck command.
RUN apk add --no-cache --virtual build-dependencies g++ musl-dev && \
    apk add --no-cache libstdc++ curl && \
    pip install -r /app/requirements.txt && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache && \
    apk del build-dependencies

WORKDIR /app

COPY . /app/sip/mock_log_publisher

ENTRYPOINT ["python3", "-m", "sip.mock_log_publisher"]
