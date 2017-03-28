#!/usr/bin/python

import socket, imaplib

# Your code goes here

SERV_IP = "192.168.17.24"
PORT = 1430
BUFF = 1024

mail = imaplib.IMAP4(SERV_IP, PORT)
mail.login("bob", "password")
mail.select("INBOX", readonly=True)
flag = mail.fetch(1, "(RFC822)")[1][0][1].split("0x")[1].split(".")[0]  # some hacky hacky goodness, because laziness
print "FLAG {0}".format(flag)
