#!/usr/bin/env python

from socket import *
import sys
import select
import os

host="0.0.0.0"
port = 9999
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf = 1024


output_dir = 'output'

# Testing to check if the file is being written
file_path1 = os.path.join(output_dir, "testing_data.txt")
f1 = open(file_path1,'wb')
info = "Initial Test Data....."
f1.write(info.encode())
f1.close()

data, addr = s.recvfrom(buf)

file_path = os.path.join(output_dir, "transfer_data.txt")

f = open(file_path,'wb')

data, addr = s.recvfrom(buf)
try:
    while(data):
        f.write(data)
        s.settimeout(2)
        data, addr = s.recvfrom(buf)
except timeout:
    f.close()
    s.close()
    print("File Downloaded")
