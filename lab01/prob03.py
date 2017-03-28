#!/usr/bin/env python

import socket,sys

TCP_IP = '0.0.0.0'
TCP_PORT = 1103
BUFFER_SIZE = 1024
MESSAGE = ""

# listen for flag
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
while 1:
    data = conn.recv(BUFFER_SIZE)
    if(data):
      print data
      conn.close()
      sys.exit(0)
