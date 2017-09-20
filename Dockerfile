FROM alpine:3.6
MAINTAINER Arjen Tamerus

COPY requirements.txt .
RUN apk add --update --no-cache gcc g++ python3 python3-dev py3-pip \
		py3-zmq py3-simplejson py3-requests \
		&& python3 -m pip install --no-cache-dir -r requirements.txt \

# Copy the SIP
COPY sip/ sip/

# Create an empty file that the Paas can use to detect being inside a swarm
COPY not_docker_swarm docker_swarm
