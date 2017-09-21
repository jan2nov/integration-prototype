#!/usr/bin/env python

from socket import *
import sys
import select
import os

output_dir = 'output'
file_path = os.path.join(output_dir, "testing_data.txt")

f = open(file_path,'wb')
data = "DAta"
f.write(data.encode())
f.close()
