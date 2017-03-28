#!/usr/bin/python

import socket
from rsa_utils import *
import md5py
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto import Random

def pad(message, blocksize):
  # returns padded message
  # mostly from https://github.com/janglin/crypto-pkcs7-example/blob/master/pkcs7.py
  l = len(message)
  output = ""
  pad_bytes = blocksize - (l % blocksize)
  padding = chr(pad_bytes) * pad_bytes
  return message + padding

def get_flag():
  ip = '192.168.17.30'
  port = 3006

  generator = 2
  p = 999959

  send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  send.connect((ip, port))
  data = send.recv(1024)
  tmp = data.split(" ")
  pubkey = int(tmp[1])

  # get the rsa variables
  # returned as dict

  # fucking test suit cant make its mind up about too small of N and too big of N.
  # phi: 16077600ERROR: This p and q are taken.  Please find another pair.
  key = gen_rsa(81, 5)
  # generat our public key
  our_pubkey = gen_pub_key(generator, key['d'], p)

  sending_pubkey = "PUBKEY {}".format(str(our_pubkey))
  send.send(sending_pubkey)

  # derive session key
  #3. Both sides then derive the session key as MD5(g^(sc) mod p).
  m = md5py.new()

  shared_secret = pow(pubkey, key['d'], p)
  m.update(str(shared_secret))
  session_key = m.hexdigest()

  # convert sessino key to bytes for AES encryption
  session_key_bytes = unhexlify(session_key)

  # 4. You can now encrypt your request ("GET FLAG") with AES-128 in CBC mode
  # you should use PKCS7 padding padding to fill the remaining bytes
  request = "GET FLAG"

  # first part of the block is the IV, so we need to extract that.
  # 128 bit blocks, 8 bits per block, 16 bytes
  BLOCK_SIZE=16
  iv = Random.new().read(BLOCK_SIZE)
  # first blobk is the Initialization Vector.
  cipher = AES.new(session_key_bytes, AES.MODE_CBC, iv)
  # TODO CHECK PADDING IS RIGHT
  ciphertext = cipher.encrypt(pad(request, BLOCK_SIZE))

  # send this to the server
  payload = iv+ciphertext 

  # Then send your encrypted request to the server as raw binary bytes.
  send.send(payload)
  data = send.recv(1024)

  # every once in a while we get this garbage
  '''
  '\xeb@\x83\xdb\x1c\x98\xf3R\x1c:S|-"\x01\xcdp\xf7\xbe+%\x85\xc2\x96u)\x9f\xb1H#\x9b\xa7'
  FLAG f5fb23681f3298f38d4c
  'XT\r\n'
  '''
  # where the server provided ciphertext is not a multiple of 16. This happens about once every 20 requests.

  # decrypt the data using AES 128 CBC
  iv = data[:BLOCK_SIZE]
  cipher = AES.new(session_key_bytes, AES.MODE_CBC, iv)
  raw = cipher.decrypt(data[BLOCK_SIZE:]).strip()
  # better way to remove padding
  pad_num = int(raw[-1].encode('hex'))
  flag = raw[:-(pad_num)]

  # all done, got the encrypted flag
  send.close()
  return flag

if __name__ == "__main__":
  get_flag()
