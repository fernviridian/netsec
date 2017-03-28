#!/usr/bin/python

import socket
import binascii
import time
import sys
from Crypto.Cipher import AES
from Crypto.Hash import MD5
import struct
from Crypto import Random

#Bob's address is 192.168.17.48, and he's listening on port 4455. Your trusted third party, the server S, is at 192.168.17.40, listening on port 4005.
#
#The protocol proceeds as follows: (Here, {xyz}_K means that xyz is encrypted with key K.)
#1. A sends to S: A, B, Na
#2. S sends to A: {Na, Kab, B, {Kab, A}_Kbs }_Kas
#3. A sends to B: {Kab, A}_Kbs
#4. B sends to A: CHALLENGE {Nb}_Kab
#5. A sends to B: RESPONSE {Nb - 1}_Kab
#6. A sends to B: GET FLAG
#7. B sends to A: FLAG flag

#The server knows you as "student" and knows Bob as "bob". So for Message 1, you might send "student bob 1234". Your secret key which you share with the server is (in hex) 20 17 04 05 20 17 04 05 20 17 04 05 20 17 04 05. All encryption is performed using AES-128 in CBC mode with PKCS7 padding.

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
	bob = connect('192.168.17.48', 4455)
	server = connect('192.168.17.40', 4005)

	# get kas key bytes
	kas = binascii.a2b_hex('20 17 04 05 20 17 04 05 20 17 04 05 20 17 04 05'.replace(' ',''))

	#1. A sends to S: A, B, Na
	na = 1234
	server.send("student bob {}".format(str(na)))

	#2. S sends to A: {Na, Kab, B, {Kab, A}_Kbs }_Kas
	server_response = server.recv(BUFFER_SIZE)
	#6bdfc15a4d2dac0a01d1e36f00e8ae61c1d14a019ef28904501e61eaba8558ee62a394c031a13646205706a0192971a9c79ffa6c50e89e40feda2fb00ab4e5040da39e48b7fcd4b334113aadc82ee8d61f10a11bf87aa904cf31e10b624c41f2de5785d8022de4b175927abba06d98ca45240269f4c6c0ff9e953d1590f31563fd1e6ef1bb26ac581bb2a65f5ad080eb4dc8e13685d215523311886af9d7b6fef95be5f8991604ea3a16f52ff45c7a83c5a48ada5854ed533601d552291810d5

	decrypted = decrypt(server_response, kas)
	#'1245 798f70a7dd9ae6b1d01b83727f0c0a46 bob 712b645873a8cee209fd3625ac24e7cb9e79002e2ce1cb369faac3e08eb48adeffd9bbf2f117a5f1c1df2755681eaaf3cd5970e87a36a66603e33b2fc89367fe'

	na_serv, kab, bob_serv, bob_request = decrypted.strip().split(" ")
	kab = binascii.a2b_hex(kab)

	#3. A sends to B: {Kab, A}_Kbs
	bob.send(bob_request)

	#4. B sends to A: CHALLENGE {Nb}_Kab
	bob_response = bob.recv(BUFFER_SIZE)
	challenge = bob_response.strip().split(" ")[1]

	# decrypt challenge
	nb = int(decrypt(challenge, kab))

	#5. A sends to B: RESPONSE {Nb - 1}_Kab
	encrypted = encrypt(pad(str(nb -1), 16), kab)
	bob.send("RESPONSE {}".format(binascii.b2a_hex(encrypted)))

	#6. A sends to B: GET FLAG
	bob.send("GET FLAG")

	#7. B sends to A: FLAG flag
	flag = bob.recv(BUFFER_SIZE)

	#clean up
	bob.close()
	server.close()
        return flag

print get_flag()
