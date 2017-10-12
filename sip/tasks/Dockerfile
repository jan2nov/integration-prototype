FROM ubuntu
MAINTAINER Nijin Thykkathu
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
COPY tests/ /home/sdp/tests/

ENTRYPOINT ["python3"]
CMD ["/home/sdp/tests/example_recv_vis_data.py", "/home/sdp/tests/vis_receiver_config.json"]
