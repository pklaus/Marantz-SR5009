#!/usr/bin/env python

import socket


TCP_IP = '192.168.1.105'
TCP_PORT = 23
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('PWON\r')
data = s.recv(BUFFER_SIZE)
s.close()

print "received data:", data