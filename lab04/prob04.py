#!/usr/bin/python

import socket
import md5py
import struct
import base64
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import binascii
from Crypto import Random


TCP_IP = '0.0.0.0'
TCP_PORT = 4404
BUFFER_SIZE = 1024
serv_flag = None
client_flag = None

def get_flag():
  return mitm()

def mitm():
  # METHOD
  #1. connect to client to get clients pubkey
  #2. send client our pubkey
  # client will now send encrypted request
  # we need to decrypt this request
  # should look like GET FLAG cookie
  # re-encrypt this request with the shared secret from the server
  # send to server

  # at the end we want the decrypted plaintext send from the server to us
  # we can then re-encrypt this with the client asymetric key

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  # our key details
  g = 2
  p = 999959
  # privkey
  d = 20
  my_pubkey = pow(g, d, p)
 
  # accept incoming conns on our open port
  conn, addr = s.accept()

  done = False
  # done when flags are captured
  serv_flag = None
  count = 0
  while not done:
    data = conn.recv(BUFFER_SIZE)
    if(data):
      SERV_IP = '192.168.17.40'
      SERV_PORT = 4004
      server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      server.connect((SERV_IP, SERV_PORT))
	 
      # we got data from the client, this should be a pubkey from the client
      client_pubkey = int(data.strip().split(" ")[1])
      # now we need to send our pubkey to the client and compute shared secret
      conn.send("PUBKEY {}".format(str(my_pubkey)))
      # what hash + AES mode for shared secret?
      # MD5 + AES CBC
      #
      
      client_shared_secret = pow(client_pubkey, d, p)
      client_request_encrypted_with_client_shared_secret = conn.recv(BUFFER_SIZE)
      client_key = binascii.a2b_hex(MD5.new(str(client_shared_secret)).hexdigest())
      # AES setup
      iv = client_request_encrypted_with_client_shared_secret[:16]
      body = client_request_encrypted_with_client_shared_secret[16:]
      a = AES.new(client_key, AES.MODE_CBC, iv)
      client_request_plaintext = a.decrypt(body)

      # now we need to do the same for the server
      serv_data = server.recv(BUFFER_SIZE)
      server_pubkey = int(serv_data.strip().split(" ")[1])
      server.send("PUBKEY {}".format(str(my_pubkey)))

      # calculate server shared secret
      server_shared_secret = pow(server_pubkey, d, p)
      server_key = binascii.a2b_hex(MD5.new(str(server_shared_secret)).hexdigest())
      # encrypt client request with our server pubkey
      BLOCK_SIZE=16
      iv = Random.new().read(BLOCK_SIZE)
      a = AES.new(server_key, AES.MODE_CBC, iv)
      ciphertext = a.encrypt(client_request_plaintext)
      server.send(iv+ciphertext)
      recv = server.recv(BUFFER_SIZE)

      # aes decrypt that response
      iv = recv[:16]
      body = recv[16:]
      a = AES.new(server_key, AES.MODE_CBC, iv)
      flag_plaintext = a.decrypt(body)
      # strip padding and print
      pad_num = int(flag_plaintext[-1].encode('hex'),16)
      flag = flag_plaintext[:-(pad_num)]
      return flag

if __name__ == '__main__':
  print get_flag()
