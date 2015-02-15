#!/usr/bin/env python

import socket
import cli

TCP_PORT = 23
BUFFER_SIZE = 1024

class SR5009(object):

    def __init__(self, hostname):
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname, TCP_PORT))

    def send(self, cmd):
        self.s.send((cmd+'\r').encode('ascii'))

    def receive(self):
        data = self.s.recv(BUFFER_SIZE)
        self.s.close()
        return data.replace('\r', '')

    @property
    def power(self):
        self.send('PW?')
        answer = self.receive()
        assert answer in ['PWON', 'PWSTANDBY']
        return answer == 'PWON'
        

def main():
    sc = cli.SR5009_CLI()
    args = sc.parse()
    s = SR5009(args.hostname)
    print("The receiver is {}.".format('on' if s.power else 'off'))

if __name__ == "__main__":
    main()


