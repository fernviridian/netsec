#!/usr/bin/python

import socket
from Crypto.Hash import SHA, HMAC
from binascii import unhexlify

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
  port = 2006

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()
  return data

def get_flag():
  # format:
  #FLAG cfe3d8cb25bcf8bc5436 445cce2ca9abca20d45e158435419d04d7b0410ad8c6dbdaa84c03a6ca6da51a
  correct = False
  key = '2017020620170206201702062017020620170206'
  b_key = unhexlify(key)

  while not correct:
    data = fetch()
    # STRIP ALL OF YOU STUPID CHARACTERS
    flag = data.split(" ")[1].rstrip("\n").strip()
    serv_hmac = data.split(" ")[2].rstrip("\n").strip()
    hmac = HMAC.new(b_key, "FLAG {0}".format(flag), SHA)
    check = hmac.hexdigest()

    if(check == serv_hmac):
      correct = True
    
  return "FLAG {0}".format(flag)
 

if __name__ == "__main__":
  get_flag()

