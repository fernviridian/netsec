#!/usr/bin/python

import socket
import binascii
import time
import sys
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import struct
from Crypto import Random

#For this problem, you can use the same trusted third party as in Problem 4. This time, your job is to get the flag from Charlie.
#Unfortunately, Charlie does not want to give you the flag. However, he is willing to share the flag with Bob.
#Charlie is listening on TCP port 4646 at 192.168.17.24.

BUFFER_SIZE = 1024

def connect(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip,port))
  return sock

def decrypt(ciphertext, key):
  # uses aes cbc
  iv = binascii.a2b_hex(ciphertext)[:16]
  body = binascii.a2b_hex(ciphertext)[16:]
  cipher = AES.new(key, AES.MODE_CBC, iv)
  decrypted = cipher.decrypt(body)
  #remove padding
  pad_num = int(decrypted[-1].encode('hex'), 16)
  decrypted = decrypted[:-(pad_num)]
  return decrypted

def encrypt(plaintext, key):
  iv = Random.new().read(16)
  cipher = AES.new(key, AES.MODE_CBC, iv)
  ciphertext = cipher.encrypt(plaintext)
  return iv + ciphertext

def pad(message, blocksize):
  # returns padded message
  # mostly from https://github.com/janglin/crypto-pkcs7-example/blob/master/pkcs7.py
  l = len(message)
  output = ""
  pad_bytes = blocksize - (l % blocksize)
  padding = chr(pad_bytes) * pad_bytes
  return message + padding

def get_flag():
	charlie = connect('192.168.17.24', 4646)

	# from bc.pcap
	#3. A sends to B: {Kab, A}_Kbs
	#b -> c: cda284a357d2e7f0ae81f88499c29820e50cbb8c3d7b669a6c5784a5667aa09d1669275067ebb1c9314c89fe9383bd966354f01ad82f46b5a0ddf09ecc40599d

	#4. B sends to A: CHALLENGE {Nb}_Kab
	#c -> b: CHALLENGE 8683 KEY 1482e4982b566028102db2635cc4f936

	#5. A sends to B: RESPONSE {Nb - 1}_Kab
	#b --> c: RESPONSE 8682 KEY 1482e4982b566028102db2635cc4f936

	#6. A sends to B: GET FLAG
	#b --> c: GET FLAG

	kab = binascii.a2b_hex('1482e4982b566028102db2635cc4f936')
	secret_request_from_bob = 'cda284a357d2e7f0ae81f88499c29820e50cbb8c3d7b669a6c5784a5667aa09d1669275067ebb1c9314c89fe9383bd966354f01ad82f46b5a0ddf09ecc40599d'

	#3. A sends to B: {Kab, A}_Kbs
	charlie.send(secret_request_from_bob)

	#4. B sends to A: CHALLENGE {Nb}_Kab
	charlie_response = charlie.recv(BUFFER_SIZE)
	challenge = charlie_response.strip().split(" ")[1]

	# decrypt challenge
	# use our old stale kab
	charlie_nonce = int(decrypt(challenge, kab))

	#5. A sends to B: RESPONSE {Nb - 1}_Kab
	encrypted = encrypt(pad(str(charlie_nonce -1), 16), kab)
	charlie.send("RESPONSE {}".format(binascii.b2a_hex(encrypted)))

	#6. A sends to B: GET FLAG
	charlie.send("GET FLAG")

	#7. B sends to A: FLAG flag
	flag = charlie.recv(BUFFER_SIZE)
	return flag

print get_flag()
