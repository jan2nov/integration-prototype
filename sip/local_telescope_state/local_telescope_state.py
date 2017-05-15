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
import pickle
import threading


class LocalTelescopeState(threading.Thread):
    def __init__(self, db=0):
        self._r = redis.StrictRedis(host='localhost', port=6379, db=db)
        self._pubsub = self._r.pubsub()
        self._default_channel = 'test'
        self._pubsub.subscribe(self._default_channel)

        self._r.publish('test', 'this will reach the listener')

    def wait_key(self, key, condition=None, timeout=None):

        def check():
            if self._r.exists(key):
                value = self._get(key)
                return condition(value)

        if condition is None:
            condition = lambda value: True
        # First need to check if the condition is already satisfied,
        # in which case don't need to create a pubsub connection
        if check():
            return
        p = self._r.pubsub()
        p.subscribe('update/' + key)

    def add(self, key, value):
        """Add a new value or pair to the model
        """
        add_value = self._r.set(key, value)
        print(add_value)

    def get(self, key):
        """Get the value from the model
        """
        get_value = self._r.get(key)
        print(get_value)

    def delete(self, key):
        """Delete the value from the model
        """
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

# Testing pickle
favorite_color = { "lion": "yellow", "kitty": "red" }


# Testing pubsub




