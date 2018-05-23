# Processing Controller Interface (Tango)

Placeholder folder for service exposing a set of Tango Devices prototyping the Processing Controller Interface to TM.

This should consist of 16 sub-array devices and a processing controller device either all serviced from the same 
Device Server or split into a pair of Device Servers, one for sub-array devices and one for the Processing Controller device.

## Quickstart


To start the tango_db and redis db use the command:

```bash
docker-compose up -d
```

This starts 3 containers:

- skasip/tango_db
- redis
- redis commander


To populate the db:

```bash
python3 -m device.db.init
```


To build test device:

```bash
docker-compose build
```

To run the test device:

```bash
docker exec --it 
```

