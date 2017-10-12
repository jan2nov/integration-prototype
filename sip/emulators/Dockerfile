# Build the image with:
#   > cd emulators/csp_visibility_sender
#   > docker build -t csp_visibility_sender .
#
# Create the container with:
#   > docker run -v $PWD:/data -p <port>:<port>/udp csp_visibility_sender /data/config.json
#
# Rerun the container with:
#   > docker start ...
#
#
# http://stackoverflow.com/questions/27596409/how-do-i-expose-a-udp-port-on-docker
#
#
FROM ubuntu:16.04
MAINTAINER Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>

# Install dependencies, and clear cache
RUN apt-get -y update \
 && apt-get -y install docker \
 python3 \
 python3-pip \
 libboost-program-options-dev \
 libboost-system-dev \
 libboost-python-dev \
 python-numpy-dev \
 dnsutils \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Set working directory
WORKDIR /home/sdp

# Copy the SIP
COPY csp_visibility_sender /home/sdp/csp_visibility_sender

# Command to run
#ENTRYPOINT ["python3", "-m", "csp_visibility_sender"]
#CMD ["/home/sdp/csp_visibility_sender/vis_sender_config.json"]

#ENTRYPOINT ["python3", "-m", "sip.emulators.csp_visibility_sender"]
#CMD ["/home/sdp/sip/etc/vis_sender_config.json", "-v"]

ENTRYPOINT ["python3", "-m"]
