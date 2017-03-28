import socket,sys
from dnslib import *

host = '192.168.17.50'
port = 1053

def get_flag():
	d = DNSRecord.question("www.flag.com")
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.sendto(d.pack(),(host,port))
	response,server = sock.recvfrom(8192)
	sock.close()
	r = DNSRecord.parse(response)
	#print r.header.id
	ip = r.a.rdata
	return "FLAG {}".format(ip)

if __name__ == "__main__":
  print get_flag()
