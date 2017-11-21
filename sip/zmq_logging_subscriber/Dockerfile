#
# zmq_logging_subscriber/Dockerfile
#
FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

# Copy python requirements file
COPY requirements.txt /app/requirements.txt

# Note
# - libstdc++ is installed as a separate step as this is needed for
#   pyzmq and should not be deleted when removing build dependencies.
# - curl is needed for the healthcheck command.
RUN apk update && \
    apk add --no-cache --virtual build-dependencies g++ musl-dev libev-dev && \
    apk add --no-cache libstdc++ curl libev && \
    pip install -r /app/requirements.txt && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache && \
    apk del build-dependencies

# Heathcheck endpoint
EXPOSE 5555

# Working directory
WORKDIR /app

# Copy code to container working directory
COPY . /app/sip/zmq_logging_subscriber

# Container heathcheck command
HEALTHCHECK --interval=15s --timeout=2s --start-period=5s --retries=2 \
    CMD curl -f http://localhost:5555/healthcheck || exit 1

# Entrypoint (command that is run default)
ENTRYPOINT ["python3", "-m", "sip.zmq_logging_subscriber"]
