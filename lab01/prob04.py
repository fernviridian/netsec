#!/usr/bin/env python

import socket

SERV_IP = '192.168.17.40'
TCP_PORT = 1104
BUFFER_SIZE = 1024
MESSAGE = "GET FLAG"

send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send.connect((SERV_IP, TCP_PORT))
send.send(MESSAGE)
data = send.recv(BUFFER_SIZE)
print data
send.close()
