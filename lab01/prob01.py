import socket, sys

UDP_IP = "192.168.17.113"
UDP_PORT = 1101

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if(data):
      print data
      sys.exit(0)
