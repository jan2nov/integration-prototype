# Processing Controller Interface (Tango)

Placeholder folder for service exposing a set of Tango Devices prototyping the Processing Controller Interface to TM.

This should consist of 16 sub-array devices and a processing controller device either all serviced from the same 
Device Server or split into a pair of Device Servers, one for sub-array devices and one for the Processing Controller device.

## Quickstart


To build the device container and mock TM client container:

```bash
docker-compose build
```

To start the tango database, redis configuration database, Processing Controller
Tango device and mock TM client: 

```bash
docker-compose up -d
```

This starts the following containers:

- **skasip/tango_mysql**: MySQL Db containing the Tango Db 
- **skasip/tango_host**: The Tango Databaseds device server
- **skasip/test_pci_device**: The Tango Processing Controller Interface device
- **redis**: A Redis instance mocking the SDP configuration database
- **rediscommander**: A web GUI for debugging the Redis configuration database
- **skasip/mock_tm_client**: A Mock TM client. 


Once these containers have started, to populate the Redis Configuration 
database run the following command (Note this will require a number of 
dependencies are installed - TODO requirements.txt file!):

```bash
python3 -m device.db.init [number of scheduling blocks]
```

To view the output of the mock TM client:


```bash
docker logs tango_tm_client_1
```

*NOTE: If the TM client has started before the PCI device it is connecting to 
is ready it is possible that the device will fail to connect. If is happens,
restart the container with the command `docker-compose up -d` and try
the `docker logs tango_tm_client_1` command again.* 


When finished all the containers can be stopped and removed with the command

```bash
docker-compose rm -s -f
```
