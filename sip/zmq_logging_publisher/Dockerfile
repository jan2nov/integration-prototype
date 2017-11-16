#
# docker build -t skasip/zlp -f sip/zmq_logging_publisher/Dockerfile sip
#
# Run with (assumes ZeroMQ Logging aggreagtor container (zla) is already running):
#
#   docker run --rm -t --name zlp --network container:zla skasip/zlp <name>
#
# Debug with:
#
#   docker run --rm -it --entrypoint=/bin/sh skasip/zlp
#

FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

# Copy python requirements.
COPY zmq_logging_publisher/requirements.txt /app/requirements.txt

# Note
# - libstdc++ is installed as a separate step as this is needed for
#   pyzmq and should not be deleted when removing build dependencies.
# - curl is needed for the healthcheck command.
RUN apk update && \
    apk add --no-cache --virtual build-dependencies g++ musl-dev && \
    apk add --no-cache libstdc++ curl && \
    pip install -r /app/requirements.txt && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache && \
    apk del build-dependencies

# Set the working directory
WORKDIR /app

# Copy source code
COPY zmq_logging_aggregator/zmq_logging_handler.py \
     /app/sip/zmq_logging_aggregator/zmq_logging_handler.py
COPY zmq_logging_publisher /app/sip/zmq_logging_publisher

# Set the default command to run.
ENTRYPOINT ["python3", "-m", "sip.zmq_logging_publisher"]
