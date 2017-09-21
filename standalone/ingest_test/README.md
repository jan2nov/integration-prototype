# Transffering data through UDP and mount docker volume in docker swarm

This is a quick test/ demo of very simple docker image thats writes a file and transfer
a file through UDP in Docker Swarm. It uses docker volume mount. It is started using 
'docker stack deploy'.

The script is very trivial, it creates a file first and then transfers a file using the 
UDP. 

Files are written to the `./output` directory with the name `testing_data` and 'transfer_data.txt'.
A cleanup script (`cleanup.sh`) is provided to remove hanging images and clean out output files.

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

