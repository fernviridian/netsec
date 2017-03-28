#!/usr/bin/python

import socket
import md5py
import struct

TCP_IP = '0.0.0.0'
TCP_PORT = 4303
BUFFER_SIZE = 1024

def get_flag():
  return init()

def init():
# listen for flag
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  # open connection to other server
  conn, addr = s.accept()
  done = False
  # done when flags are captured
  serv_flag = None
  count = 0
  while not done:
    data = conn.recv(BUFFER_SIZE)
    if(data):
      SERV_IP = '192.168.17.40'
      SERV_PORT = 4003
      send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      send.connect((SERV_IP, SERV_PORT))

      # server receieved data
      # proxy to other server
      # send flag data to server
      orig_hash = data.strip().split(" ")[-1]
      orig_msg = " ".join(data.strip().split(" ")[0:-1])

      # setup our md5 block state based on the old md5 hash
      A = socket.htonl(long(orig_hash[0:8], 16))
      B = socket.htonl(long(orig_hash[8:16], 16))
      C = socket.htonl(long(orig_hash[16:24], 16))
      D = socket.htonl(long(orig_hash[24:32], 16))

      # padding and such
      orig_msg_len = len(orig_msg)
      # -1 is to account for magic 0x80
      padding_len = 64 - 8 - 8 - orig_msg_len - 1

      # if we have less than 0 padding, we need to shift by 64 bytes until we have a positive
      while padding_len < 0:
        padding_len += 64

      # the magical delimited that is added after our message according to skullsec blog
      #orig_msg + '\x80'
      #now we need to pad with our padding_length
      #orig_msg += '\x00' * padding_len
      orig_msg += struct.pack('1s', '\x80')
      orig_msg += struct.pack(str(padding_len) + "s", '\x00')

      # we need to compute how many bits for our struct packing
      # unsigned long long is 8 bits
      bitsize = (orig_msg_len + 8) * 8

      # make it little-endian!!!! with unsigned long long
      orig_msg += struct.pack('<Q', bitsize)

      # create our md5 object
      forged = md5py.MD5()
      forged.update('A'*8 + orig_msg)
      forged.A = A
      forged.B = B
      forged.C = C
      forged.D = D
      # append our nasties
      forged.update(" FLAG")
      forged_hash = forged.hexdigest()
      
      new_msg = "{0} FLAG {1}".format(orig_msg, forged_hash)
      send.send(new_msg)
      servdata = send.recv(BUFFER_SIZE)
      # send server command back to client
      flag = servdata.split("FLAG: ")[1].strip()
      flag = "FLAG {}".format(flag)
      return flag

  send.close()
  conn.close()

if __name__ == '__main__':
  print get_flag()
