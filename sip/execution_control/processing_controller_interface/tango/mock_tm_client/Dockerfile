FROM ubuntu:17.10

RUN apt-get update && apt-get install -y python3-tango

WORKDIR /tm_client

COPY app.py /tm_client

ENTRYPOINT ["python3", "-u", "app.py"]

