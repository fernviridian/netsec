#!/usr/bin/python

import socket
from Crypto.Hash import SHA, HMAC
from binascii import unhexlify
import md5
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

def fetch():
  ip = '192.168.17.200'
  port = 2007
  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  send.send("GET FLAG")
  data = send.recv(1024)
  send.close()
  return data

def get_passwords():
  filename = '/usr/share/dict/words'
  l = []
  f = open(filename)
  for password in f:
   l.append(password.strip().lower()) 
  f.close()
  return l

def hash_password(password):
  m = md5.new(password)
  return m.hexdigest()

def get_flag():
  data = fetch()
  # STRIP ALL OF YOU STUPID CHARACTERS
  flag = data.rstrip("\n").strip()
  
  BLOCK_SIZE = 16
  iv = flag[:BLOCK_SIZE]

  # AES-128
  # password is md5
  passwords = get_passwords()

  for password in passwords:
    md5_pass = hash_password(password)
    # AES stuff
    cipher = AES.new(unhexlify(md5_pass), AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(data[BLOCK_SIZE:]) 
    '''password unsophisticated md5 4f17816386fca245b2ad175bc79fb81f
    decrypted: FLAG 268ee2cb2a37b267220b'''
    if("FLAG" in decrypted):
      break

  # remove padding
  raw = decrypted.strip()
  pad_num = int(raw[-1].encode('hex'))
  flag = raw[:-(pad_num)]
  return flag


if __name__ == "__main__":
  get_flag()

