#!/usr/bin/python

import socket
from rsa_utils import *

def get_flag():
  ip = '192.168.17.30'
  port = 3003

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  key = gen_rsa(81, 5)
  send.send("GET FLAG {0} {1}".format(key['N'], key['e']))
  data = send.recv(1024)
  tmp = data.split(" ")
  #KEYLENGTH: 16
  flag = int(tmp[1].strip())
  hex_flag = bit_to_hex(decrypt(flag, key['N'], key['d']))
  return "FLAG {0}".format(hex_flag)

if __name__ == "__main__":
  get_flag()
