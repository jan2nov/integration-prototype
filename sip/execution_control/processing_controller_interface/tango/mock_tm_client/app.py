# -*- coding: utf-8 -*-
"""Mock client Application for the PCI device.

This is a placeholder for a TM client application / emulator."""


import tango
import time


def main():
    dev = tango.DeviceProxy('sip_SDP/test/1')
    while True:
        print(dev.time, dev.num_scheduling_blocks)
        time.sleep(1)


if __name__ == '__main__':
    main()
