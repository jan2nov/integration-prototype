FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

# Copy python requirements.
COPY requirements.txt /app/requirements.txt

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
COPY . /app/sip/zmq_logging_forwarder

# ZMQ.XSUB port (Publishers should connect to this)
EXPOSE 5559

# ZMQ.XPUB port (Subscribers should connect to this)
EXPOSE 5560

# Healthcheck port
EXPOSE 5555

# Container heathcheck command
HEALTHCHECK --interval=15s --timeout=2s --start-period=5s --retries=2 \
    CMD curl -f http://localhost:5555/healthcheck || exit 1

# Set the default command to run.
ENTRYPOINT ["python3", "-m", "sip.zmq_logging_forwarder"]
