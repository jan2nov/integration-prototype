#
# docker build -t sip/zla sip/zmq_logging_aggregator
#
# Test interactively with:
#   docker run --rm -it --entrypoint=/bin/sh sip/zla
#
# Run and show logging:
#   docker run --rm -t -p 5555:5555 -p 9020:9020 -p 9030:9030 --name zla sip/zla
#

FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

COPY requirements.txt /app/requirements.txt

# Note
# - libstdc++ is installed as a separate step as this is needed for
#   pyzmq and should not be deleted when removing build dependencies.
# - curl is needed for the healthcheck command.
RUN apk add --no-cache --virtual build-dependencies g++ musl-dev libev-dev && \
    apk add --no-cache libstdc++ curl libev && \
    pip install -r /app/requirements.txt && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache && \
    apk del build-dependencies

# Python logging.handlers.DEFAULT_TCP_LOGGING_PORT
EXPOSE 9020

# Flask server port
EXPOSE 5555

# Python logging configuration server
EXPOSE 9030

WORKDIR /app

HEALTHCHECK --interval=5s --timeout=2s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5555/healthcheck || exit 1

COPY . /app/sip/zla

ENTRYPOINT ["python3"]
CMD ["-m", "sip.zla"]
