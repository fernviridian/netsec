#!/usr/bin/python

import socket
from rsa_utils import *

def get_flag():
  ip = '192.168.17.30'
  port = 3002

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  data = send.recv(1024)
  tmp = data.split(" ")
  #KEYLENGTH: 16
  length = int(tmp[1])

  # chekc that d is not negative
  # check that d is not bigger than phiN

  # get the rsa variables
  # returned as dict

  # fucking test suit cant make its mind up about too small of N and too big of N.
  # phi: 16077600ERROR: This p and q are taken.  Please find another pair.
  returned = gen_rsa(length, 3)

  # send the messages to the server
  p_send = "p: {}".format(returned['p'])
  q_send = "q: {}".format(returned['q'])
  n_send = "N: {}".format(returned['N'])
  e_send = "e: {}".format(returned['e'])
  d_send = "d: {}".format(returned['d'])

  s = pretty_print(returned)
  send.send(s) 
  data = send.recv(1024)
  if ('OK' in data):
    send.send("GET FLAG")
    flag = send.recv(1024).strip()
    return flag

if __name__ == "__main__":
  get_flag()
