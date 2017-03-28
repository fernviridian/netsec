#!/usr/bin/python

import socket
from rsa_utils import *

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
def get_flag():
  ip = '192.168.17.30'
  port = 3004

  N = 3110232614083941699686461
  e = 3

  good = False
  while not good:
    send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send.connect((ip, port))
    send.send("GET FLAG")
    data = send.recv(1024)
    send.close()
    tmp = data.split(" ")
    flag = int(tmp[1])
    sig = int(tmp[2])
    good = verify_signature(flag, sig, N, e)

  # now we have a matching flag

  f = "%x" % flag
  return "FLAG {}".format(f)

if __name__ == "__main__":
  get_flag()
