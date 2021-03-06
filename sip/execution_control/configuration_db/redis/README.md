# SIP Configuration Service (Redis variant)

## Roles and responsibilities

The SIP Configuration Database Service provides a backing service for storing
data used by the different Execution Control Service components and currently
also provides limited event queue like capability for communicating events
between the Processing Controller Interface service and Scheduler. The choice
of database technology used by this service (currently Redis) is hidden from
other Execution Control Services by means of a configuration database client
API. This provides a set of modules which abstract all details of how
information is stored in the database from the client Services. The client
library is written as a low level abstraction layer on top of the database
Python API and a set of higher level functions providing a view on the data
more tuned to be more appropriate for use by the various Execution Control
Services.

Design notes for this service can be found in the
[SIP Execution Control Confluence pages](https://confluence.ska-sdp.org/display/WBS/SIP%3A+%5BEC%5D+Configuration+Database+Service)

## Quickstart

To start Docker containers for a Redis Db instance (with a persistent volume)
as well as a [Redis Commander](https://github.com/joeferner/redis-commander)
instance (useful for debugging) issue the following command:  

```bash
docker-compose up -d
```

This will deploy the containers to the local Docker installation. If 
wanting to deploy to Docker Swarm instead use the following command: 


```bash
docker stack deploy -c docker-compose.yml [stack name]
```

Once finished, to stop this service and remove its running containers, if
started using `docker-compose` (with the local Docker engine) issue the
command:

```bash
docker-compose rm -s -f
```

or if using Docker Swarm mode:

```bash
docker stack rm [stack name]
```

It is also possible to run redis server natively (without Docker). This is
useful for development and debugging.

Start redis server
```bash
redis-server
```

Note - It requires redis to be installed and all python packages in the
requirements.txt file

### Utility Scripts

To set initial data into the configuration database run the following command:

```bash
python3 -m db_client.utils.set_initial_data
```

### Test Scripts

To test the Master Controller db client run the following command:

```bash
python3 -m db_client.tests.test_master_client
```

To run examples demonstrating the use of the Processing Controller client 
run the following command

```bash
python3 -m db_client.tests.processing_controller_client_example
```
