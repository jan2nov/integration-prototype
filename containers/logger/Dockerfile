ARG tag=latest
FROM sip-base:$tag
MAINTAINER Arjen Tamerus

# Copy the SIP
COPY sip/common sip/common
COPY sip/slave sip/slave

# Create an empty file that the Paas can use to detect being inside a swarm
COPY not_docker_swarm docker_swarm
