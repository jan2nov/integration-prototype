#
# docker build -t sip/zla -f sip/service_zmq_logging_aggregator/Dockerfile .
#
# Test with:
#   docker run --rm -it --entrypoint=/bin/sh sip/zla
#
# Run and show logging:
#   docker run --rm -t --name zla sip/zla
#

FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

COPY sip/service_zmq_logging_aggregator/requirements.txt /app/requirements.txt

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

EXPOSE 5555

WORKDIR /app

HEALTHCHECK --interval=5s --timeout=2s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5555/health || exit 1

COPY sip/service_zmq_logging_aggregator /app/zla

ENTRYPOINT ["python3"]
CMD ["-m", "zla"]
