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
  flag = "FLAG ..."

  # Your code to get the flag goes here

  # The expected format is "FLAG <flag>" where <flag> is the 
  # actual flag that you receive from the problem environment.
  return flag


if __name__ == "__main__":
  get_flag()

