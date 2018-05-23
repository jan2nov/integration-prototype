#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Tango device server

Run (from the "processing_controller_interface/tango" folder) with:

    python3 -m device.run

The first argument has to match the device server in the form <class>/arg

ie as we have registered the device 'sip_SDP/test/1' with device server
'Test/test'

and the device class here is 'Test' the first argument has to be 'test'

Once this has started the device can be queried with the name it was registered
as, ie. 'sip_sdp/test/1'

    import tango
    db = tango.Database()
    db.get_device_info("sip_SDP/test/1")

The device can then be connected to using the client API
http://pytango.readthedocs.io/en/stable/client_api/device_proxy.html
eg:

    import tango
    dev = tango.DeviceProxy('sip_SDP/test/1')
    print(dev.time)
    print(dev.echo('hello world'))
    print(dev.info())
    print(dev.attribute_query('time')
"""
import time
from tango import AttrWriteType
from tango.server import run, Device, DeviceMeta, attribute, command
from tango import Database, DbDevInfo
from .db.client import ConfigDbClient

DB = ConfigDbClient()


class Test(Device, metaclass=DeviceMeta):
    """Test Tango device class."""

    _value = [1, 2, 3]

    @attribute
    def time(self):
        return time.time()

    @command(dtype_in=str, dtype_out=str)
    def echo(self, value):
        return value

    @attribute(dtype=int, access=AttrWriteType.READ)
    def num_scheduling_blocks(self):
        return len(DB.get_scheduling_block_ids())

    @command(dtype_in=int, dtype_out=str)
    def get_sbi_id(self, value):
        sbi_ids = DB.get_scheduling_block_ids()
        return sbi_ids[value]

    @attribute(dtype=(int, ), max_dim_x=10, access=AttrWriteType.READ_WRITE)
    def test(self):
        return self._value

    @test.write
    def test(self, value):
        self._value = value


if __name__ == '__main__':

    # Register the device with the TANGO database.
    # FIXME(BM) work out way to only do this if the device is not already \
    # registered
    TANGO_DB = Database()
    DEV_INFO = DbDevInfo()
    DEV_INFO.name = 'sip_SDP/test/1'
    DEV_INFO._class = 'Test'
    DEV_INFO.server = 'Test/test'
    print('Adding device: %s' % DEV_INFO.name)
    TANGO_DB.add_device(DEV_INFO)

    # Start the device server
    Test.run_server(['test'])

