ARG tag=latest
FROM sip-numpy-base:$tag
MAINTAINER Arjen Tamerus

#RUN apk add --update --no-cache py3-numpy

# Copy the SIP
COPY sip sip

# Create an empty file that the Paas can use to detect being inside a swarm
RUN touch docker_swarm
