#!/usr/bin/python

import socket

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
  port = 3000

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()
  tmp = data.split(" ")
  #FLAG 1049491169825362370105756

  dec = int(tmp[1])
  flag = "%x" % dec
  return "FLAG {}".format(flag)

if __name__ == "__main__":
  print get_flag()
