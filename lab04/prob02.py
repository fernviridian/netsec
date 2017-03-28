#!/usr/bin/python

import socket

# Your code goes here

# forward packets to 192.168.17.40 port 4001
# listen on tcp 4101

# There are two flags for this problem: one from the server and one from the client. You can extract them from the messages passed back and forth, but to obtain the flags, you must pass each message accurately and without too much delay.

#student@dojo:~/labs/lab04$
TCP_IP = '0.0.0.0'
TCP_PORT = 4202
BUFFER_SIZE = 1024
serv_flag = None
client_flag = None

def get_flag():
  return init()

def xor(xs, ys):
    maxlen = max(len(xs), len(ys))
    if len(xs) < maxlen:
        xs += '\x00' * (maxlen - len(xs))
    else:
        ys += '\x00' * (maxlen - len(ys))
    x = ""
    for i in range(0,maxlen):
        x += chr(ord(xs[i]) ^ ord(ys[i]))
    return x

def init():
# listen for flag
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  # open connection to other server

  conn, addr = s.accept()
  done = False
  # done when flags are captured
  serv_flag = None
  count = 0
  while not done:
    data = conn.recv(BUFFER_SIZE)
    if(data):
      SERV_IP = '192.168.17.40'
      SERV_PORT = 4002
      send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      send.connect((SERV_IP, SERV_PORT))
 
      # server receieved data
      # proxy to other server
      # send flag data to server
      iv = data[:16]
      body = data[16:]
      plaintext = "GET DOG FROG GRIP STOP FLY"
      desired = "GET DOG FLAG GRIP STOP FLY"
      attack = xor(plaintext, desired)
      payload = xor(body.strip(), attack)
      send.send(iv+payload)
      servdata = send.recv(BUFFER_SIZE)
      flag = servdata.split("FLAG: ")[1].split(" ")[0].split("\n")[0].strip()
      return "FLAG {}".format(flag)

print get_flag()

#student@dojo:~/labs/lab04$ python prob02.py
#data: '4\xbb-\x93\xfdbK\x1c$\xe8\x12\xb6\xa1\xc9\n,\xb2\xebR\xe9\x87\xf9\\\xd4\xd85s\xf0K\x01\x8am\x06\xb2Lv\xbb\xfaf\x12\x1ce\x03QI\x9fPN'
#attack string: '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1e\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#payload: '\xb2\xebR\xe9\x87\xf9\\\xd4\xd8+}\xf0K\x01\x8am\x06\xb2Lv\xbb\xfaf\x12\x1ce\x03QI\x9fPN'
#FLAG 52c9c3489c2e7cbb78f3
#GRIP: got it
#STOP: hammertime | collaborate listen
#FLY: bzzz
#
#servdata: DOG: woof!
#FLAG: 52c9c3489c2e7cbb78f3
#GRIP: got it
#STOP: hammertime | collaborate listen
#FLY: bzzz#
