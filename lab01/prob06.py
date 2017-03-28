#!/usr/bin/python

import socket, sys

# Your code goes here

'''
27 + 7 = ?
34
OK
GET FLAG
FLAG a90e631a55b6ffeb
'''

SERV_IP = '192.168.17.60'
TCP_PORT = 1106
BUFFER_SIZE = 1024
MESSAGE = "GET FLAG"

def get_flag():
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((SERV_IP, TCP_PORT))
  data = send.recv(BUFFER_SIZE)
  # challenge
  num1 = int(data.split(" ")[0])
  num2 = int(data.split(" ")[2])
  op = data.split(" ")[1]
  if(op == "/"):
    answer = num1/num2
  elif(op == "*"):
    answer = num1*num2
  elif(op == "+"):
    answer = num1+num2
  elif(op == "-"):
    answer = num1-num2
  send.send(str(answer))
  data = send.recv(BUFFER_SIZE)
  send.send(MESSAGE)
  data = send.recv(BUFFER_SIZE)
  return data
    
print get_flag()
sys.exit(0)
