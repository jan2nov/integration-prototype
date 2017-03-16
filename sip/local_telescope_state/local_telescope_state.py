#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Local Telescope State service module.

"""

import os
import sys
import time
import argparse
import numpy
import redis


class LocalTelescopeState(object):
    def __init__(self, db=0):
        print("Hello World")
        self._r = redis.StrictRedis(host='localhost', port=6379, db=db)

    def add(self, key, value):
        add_value = self._r.set(key, value)
        print(add_value)

    def get(self, key):
        get_value = self._r.get(key)
        print(get_value)

    def delete(self, key):
        return self._r.delete(key)


# Testing the Local Telescope State class
test = LocalTelescopeState()
key_value = "foo"
data = "bar"
new_value = "delete"
new_data = "data"

# Adding and Query key_value
test.add(key_value, data)
test.get(key_value)

# Adding, quering and deleting new_value
test.add(new_value, new_data)
test.get(new_value)
test.delete(new_value)
