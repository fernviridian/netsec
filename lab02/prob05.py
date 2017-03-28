#!/usr/bin/python

import socket
import hashlib

#
# get_flag() - This is the function that will be called by the automated
#              grading script.  Upon each invocation, it should dynamically
#              interact with the lab environment to capture and return the
#              flag.  So, for example, if I run this from my "student" VM,
#              it should return my flag for the given problem.  As another
#              example, any solution that simply hard-codes a flag found
#              through interactive exploration (eg using netcat/telnet)
#              should expect to fail the test suite and receive zero points
#              for the code portion of the grade.

def fetch():
  ip = '192.168.17.200'
  port = 2005

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()
  return data

def get_flag():
  # format:
  #FLAG cfe3d8cb25bcf8bc5436 445cce2ca9abca20d45e158435419d04d7b0410ad8c6dbdaa84c03a6ca6da51a
  '''
  FLAG 71d32719988f57776960 8070739d99b14f4b095d14ad1f9af67d802355a31f57e5c2b8e5178ea4c01d32

  8070739d99b14f4b095d14ad1f9af67d802355a31f57e5c2b8e5178ea4c01d32
  '''
  correct = False

  while not correct:
    data = fetch()
    # STRIP ALL OF YOU STUPID CHARACTERS
    flag = data.split(" ")[1].rstrip("\n").strip()
    serv_hash = data.split(" ")[2].rstrip("\n").strip()
    h = hashlib.sha256("FLAG {}".format(flag).rstrip("\n").strip())
    check = h.hexdigest().strip()
    if(check == serv_hash):
      correct = True

  return "FLAG {0}".format(flag)
 

if __name__ == "__main__":
  get_flag()

