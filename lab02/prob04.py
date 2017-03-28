#!/usr/bin/python

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
  key = '20170204201702042017020420170204'
  
  ip = '192.168.17.200'
  port = 2004

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()

  b_key = unhexlify(key)

  # first part of the block is the IV, so we need to extract that.
  # 128 bit blocks, 8 bits per block, 16 bytes
  BLOCK_SIZE=16
  iv = data[:BLOCK_SIZE]
  cipher = AES.new(b_key, AES.MODE_CBC, iv)
  raw = cipher.decrypt(data[BLOCK_SIZE:]).strip()
  pad_num = int(raw[-1].encode('hex'))
  flag = raw[:-(pad_num)]

  return flag

if __name__ == "__main__":
  get_flag()
