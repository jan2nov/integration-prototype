FROM alpine:3.6
LABEL maintainer="Arjen Tamerus"

WORKDIR app

COPY requirements.txt .
RUN apk add --update --no-cache gcc g++ python3 python3-dev py3-pip \
		py3-zmq py3-simplejson py3-requests \
		&& python3 -m pip install --no-cache-dir -r requirements.txt 

# Copy the SIP
ADD sip/master/ sip/master
ADD sip/common/ sip/common
ADD sip/etc/ sip/etc

# Create an empty file that the Paas can use to detect being inside a swarm
RUN touch docker_swarm

ENTRYPOINT python3 -m sip.master
