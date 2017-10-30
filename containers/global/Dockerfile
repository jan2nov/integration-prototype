ARG tag=latest
FROM sip-base:$tag
MAINTAINER Arjen Tamerus

#RUN apk add --update --no-cache py3-numpy

# Copy the SIP
COPY sip/common sip/common
COPY sip/slave sip/slave

# Create an empty file that the Paas can use to detect being inside a swarm
COPY not_docker_swarm docker_swarm
