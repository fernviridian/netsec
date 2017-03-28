#!/usr/bin/python::ww

import socket
from binascii import unhexlify
from Crypto.Cipher import AES

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
  port = 2003

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()

  # Your code to get the flag goes here
  key = "20170203201702032017020320170203"
  b_key = unhexlify(key)

  # first part of the block is the IV, so we need to extract that.
  #MODE_ECB, no iv
  cipher = AES.new(b_key, AES.MODE_ECB)
  raw = cipher.decrypt(data).strip()
  pad_num = int(raw[-1].encode('hex'))
  flag = raw[:-(pad_num)] 

  # The expected format is "FLAG <flag>" where <flag> is the 
  # actual flag that you receive from the problem environment.
  return flag

if __name__ == "__main__":
  get_flag()

