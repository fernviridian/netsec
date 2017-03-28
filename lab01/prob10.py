#!/usr/bin/python

import socket
from Queue import Queue
from threading import Thread

# OMG so much threading all up in this place
# why did I do this to myself....????!?!?
# the result is a very fast port scanner that took way too much engineering time
# I guess it was for the LEARNZ
#student@dojo:~/labs/lab01$ time python prob10.py
#[28163]
#FLAG 8ce8e221097dce76
#[1]+  Killed                  python prob10.py

#real    1m44.753s   #nottoobad
#user    0m3.516s
#sys     0m2.596s

MIN = 2000
MAX = 60000
PORT = 28163
IP="192.168.17.50"
BUFFER_SIZE = 1024
DELAY = 0.2
MESSAGE = "GET FLAG"

'''
student@dojo:~/labs/lab01$ python prob10.py
Port 1105:       Open
Port 28163:      Open
'''

def connect(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(DELAY)
    try:
      sock.connect((IP, port))
      sock.close()
      return port
    except:
      sock.close()
      return None

# scan for ports
# find_open_ports(1024,65535)
def get_flag(port):
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((IP, port))
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

open_port = []

def worker():
    while True:
        port = q.get()
        s = connect(port)
	if s is not None:
	    open_port.append(port)
        q.task_done()

q = Queue()
workers = 60
for i in range(workers):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for port in range(MIN, MAX):
    q.put(port)

q.join()

print get_flag(open_port[0])
