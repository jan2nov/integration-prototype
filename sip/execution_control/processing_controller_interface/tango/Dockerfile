FROM ubuntu:17.10

RUN apt-get update && apt-get install -y python3-tango
RUN apt-get install -y python3-pip
RUN pip3 install jsonschema redis

WORKDIR /pci

COPY ./device /pci/device

ENTRYPOINT ["python3", "-m", "device.run"]

