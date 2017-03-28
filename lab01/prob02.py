import socket,sys

UDP_IP = "192.168.17.113"
SERV_IP = '192.168.17.200'
UDP_PORT = 1102
MESSAGE = "GETFLAG"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.sendto(MESSAGE, (SERV_IP, UDP_PORT))

listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
listen.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = listen.recvfrom(1024) # buffer size is 1024 bytes
    if(data):
      print data
      sys.exit(0)
