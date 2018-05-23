#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test Tango device server

Run with

./device.py test

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
from tango.server import Device, DeviceMeta, attribute, command, pipe
from .db.client import ConfigDbClient

DB = ConfigDbClient()


class Test(Device, metaclass=DeviceMeta):
    """Test Tango device class."""

    @attribute
    def time(self):
        return time.time()

    @command(dtype_in=str, dtype_out=str)
    def echo(self, value):
        return value

    @pipe
    def info(self):
        sbi_ids = DB.get_scheduling_block_ids()
        return 'Information', dict(foo=2, bar='hello', sbi_ids=sbi_ids)


if __name__ == '__main__':
    Test.run_server()
