# docker build -t file_writer .

# Create a volume:
# docker volume create my-vol
# docker run -it --rm --name test --mount source=my-vol,target=/app file_writer
#
# Bind-mount the current directory to the container /app directory.
# docker run -it --rm --name test --mount type=bind,source="$(pwd)",target=/app file_writer
#
# Run as a service on swarm:
# docker service create --detach=true --replicas 2 --restart-condition none --mount type=bind,source="$(pwd)",target=/app file_writer
#
#

FROM python:3.6.2-alpine3.6
LABEL maintainer="Nijin Thykkathu <nijin.thykkathu@stfc.ac.uk>"
RUN pip install requests ntplib
WORKDIR /app
COPY udp_recv.py /app/udp_recv.py
COPY udp_sender.py /app/udp_sender.py
COPY mytext.txt /app/mytext.txt
#COPY test_file.py /app/test_file.py
ENTRYPOINT ["python3"]
#CMD ["test_file.py"]
#CMD ["udp_recv.py"]
