# Transferring data using UDP in Docker Swarm and uses docker volume

This is a quick test/ demo of very simple docker image that writes a file and transfer
a file through UDP in Docker Swarm. It uses docker volume mount. It is started using
'docker stack deploy'.

The script is very trivial, it creates a file first (just for test purpose) and then
transfers a file using the UDP. Currently only uses one node (local machine). Next plan is to expand
into 2 nodes (2 VMS) and test it.

Files are written to the `./output` directory with the name `testing_data` and 'transfer_data.txt'.
A cleanup script (`cleanup.sh`) is provided to remove hanging images and clean out output files.

The output file could be found in var/lib/docker/volumes/<volume_name>/_data

## 1. Set up virtualenv

```shell
virtualenv -p `which python3` venv
. venv/bin/activate
pip install -r requirements
```

## 2. Build the image

```shell
docker build -t ingest_test .
```

## 3. Create docker volume

```shell
docker volume create my-test
```

## 4. Start the server as a service 

*Note: Make sure the image has been built first see section 2.*

```shell
docker stack deploy -c docker-stack.yml test
```

## 5. Start the sender as a service 

*Note: Make sure the image has been built first see section 2.*

```shell
docker stack deploy -c docker-sender.yml sender
```

## 6. Remove the service

```shell
docker service rm <service id>
```

## 7. Interact with the service 

docker exec -it <servicename> ash

