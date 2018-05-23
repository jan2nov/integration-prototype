FROM ubuntu:17.10

WORKDIR /pci

RUN apt-get update && apt-get install -y python3-tango
RUN apt-get install -y python3-pip
RUN pip3 install jsonschema redis

CMD ["sleep", "3600"]
