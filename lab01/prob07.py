#!/usr/bin/python

import socket, sys

# Your code goes here

'''
student@dojo:~/labs/lab01$ nc 192.168.17.200 1107
GET FLAG
GOTO 192.168.17.217:1107
student@dojo:~/labs/lab01$ nc 192.168.17.217 1107
GET FLAG
GOTO 192.168.17.203:1107
student@dojo:~/labs/lab01$ nc 192.168.17.203 1107
GET FLAG
FLAG e73dfc6e3ca6a32e
'''

SERV_IP = '192.168.17.200'
TCP_PORT = 1107
BUFFER_SIZE = 1024
MESSAGE = "GET FLAG"

def get_flag():
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((SERV_IP, TCP_PORT))
  # challenge
  send.send(MESSAGE)
  data = send.recv(BUFFER_SIZE)
  return data

flag = False
while not flag:
  message = get_flag()
  if ("GOTO" in message):
    temp = message.split(" ")[1].split(":")
    SERV_IP = temp[0]
    TCP_PORT = int(temp[1])
    get_flag()
  else:
    # got flag
    print message
    sys.exit(0)
