FROM alpine:3.6
LABEL maintainer="Arjen Tamerus"

WORKDIR app

ADD containers/base/requirements.txt .
RUN apk add --update --no-cache python3 py3-pip \
		py3-zmq py3-simplejson \
		&& python3 -m pip install --no-cache-dir -r requirements.txt 

# Copy the SIP essentials
ADD sip/etc/ sip/etc

# Create an empty file that the Paas can use to detect being inside a swarm
RUN touch docker_swarm
