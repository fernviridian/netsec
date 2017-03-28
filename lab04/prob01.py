#!/usr/bin/python

import socket

# Your code goes here

# forward packets to 192.168.17.40 port 4001
# listen on tcp 4101

# There are two flags for this problem: one from the server and one from the client. You can extract them from the messages passed back and forth, but to obtain the flags, you must pass each message accurately and without too much delay.

#student@dojo:~/labs/lab04$ nc -l 4101
#GET FLAG 35427695 1f0a195067a0a38a05ac072492a9058b
#student@dojo:~/labs/lab04$ nc -l 4101
#SERVER FLAG 68447044a8c446dba736 35427695 7f5519d54b2d1df58b20341adf500c6c
#^C
#student@dojo:~/labs/lab04$
TCP_IP = '0.0.0.0'
TCP_PORT = 4101
BUFFER_SIZE = 1024
serv_flag = None
client_flag = None

def get_flag():
  return init()

def init():
# listen for flag
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  # open connection to other server

  SERV_IP = '192.168.17.40'
  SERV_PORT = 4001
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((SERV_IP, SERV_PORT))
  #send.send(MESSAGE)
  #data = send.recv(BUFFER_SIZE)
  #print data
  #send.close()

  conn, addr = s.accept()
  done = False
  # done when flags are captured
  while not done:
    data = conn.recv(BUFFER_SIZE)
    if(data):
      # server receieved data
      # proxy to other server
      # send flag data to server
      send.send(data)
      servdata = send.recv(BUFFER_SIZE)
      serv_flag = parse_server_flag(servdata)
      # send server command back to client
      conn.send(servdata)
      cflag = conn.recv(BUFFER_SIZE)
      client_flag = parse_client_flag(cflag)

    if(serv_flag and client_flag):
      done = True

  send.close()
  conn.close()
  return "SERVER-FLAG {0}\nCLIENT-FLAG {1}".format(serv_flag, client_flag)

def parse_server_flag(flag):
  if "SERVER FLAG" in flag:
    return " ".join(flag.split(" ")[2:3])
  else:
    return None

def parse_client_flag(flag):
  if "FLAG" in flag:
    return " ".join(flag.split(" ")[2:3])
  else:
    return None

print get_flag()
