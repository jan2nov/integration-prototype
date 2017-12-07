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
 wget \
 make \
 dnsutils \
 && rm -rf /var/lib/apt/lists/*

# Install Redis.
RUN \
  cd /tmp && \
  wget http://download.redis.io/redis-stable.tar.gz && \
  tar xvzf redis-stable.tar.gz && \
  cd redis-stable && \
  make && \
  make install && \
  cp -f src/redis-sentinel /usr/local/bin && \
  mkdir -p /etc/redis && \
  cp -f *.conf /etc/redis && \
  rm -rf /tmp/redis-stable* && \
  sed -i 's/^\(bind .*\)$/# \1/' /etc/redis/redis.conf && \
  sed -i 's/^\(daemonize .*\)$/# \1/' /etc/redis/redis.conf && \
  sed -i 's/^\(dir .*\)$/# \1\ndir \/data/' /etc/redis/redis.conf && \
  sed -i 's/^\(logfile .*\)$/# \1/' /etc/redis/redis.conf

# Define mountable directories.
VOLUME ["/data"]

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Set working directory
WORKDIR /home/sdp

# Copy the SIP
#COPY sip/ sip/
COPY tools/csp_visibility_sender/ csp_visibility_sender/
COPY vis_receiver/ vis_receiver/
COPY config_database/redis redis/

# Adding Redis to PYTHONPath
ENV PYTHONPATH $PYTHONPATH:/home/sdp/redis

