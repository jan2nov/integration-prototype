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
docker exec --it tango_test_device_1 /bin/bash
python3 -m device.register
python3 -m device.run test
```

Optionally, before running the device use:

```bash
python3 -m device.db.init 5
```

to add 5 scheduling block instances into the configuration 
database.


To connect to the test device:

```bash
docker exec --it tango_test_device_1 /bin/bash
python3
```

Then in the python3 prompt:

```python
import tango
dev = tango.DeviceProxy('sip_SDP/test/1')
dev.time
dev.test
dev.test = [4, 5, 6]
dev.test
dev.echo('hello')
dev.num_scheduling_blocks
dev.get_sbi_id(0)
```


