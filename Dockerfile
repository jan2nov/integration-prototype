FROM ubuntu
MAINTAINER David Terrett
USER root

RUN adduser --disabled-password -gecos 'unprivileged user' sdp

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
#COPY sip/ sip/
COPY tools/csp_visibility_sender/ csp_visibility_sender/
COPY vis_receiver/ vis_receiver/
COPY config_database/ config_database/

