#!/usr/bin/python

import socket, binascii
import base64

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
  ip = '192.168.17.200'
  port = 2002

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()
  tmp = data.split(" ")
  length = int(tmp[1])
  #flag = binascii.b2a_base64("FLAG {}".format(tmp[2]).strip("\n"))
  b64_flag = base64.b64encode(tmp[2][:length].strip("\n"))
  return "FLAG {}".format(b64_flag)

if __name__ == "__main__":
  get_flag()

