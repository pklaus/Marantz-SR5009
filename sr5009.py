#!/usr/bin/env python

import socket
import cli
import logging
import select
import time

logger = logging.getLogger(__name__)


class SR5009(object):

    TCP_PORT = 23
    BUFFER_SIZE = 1024
    LINE_TERMINATOR = '\r'
    WAIT_AFTER_SEND = 10E-3

    def __init__(self, hostname):
        self.hostname = hostname
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((hostname, self.TCP_PORT))
        #self.s.settimeout(0) # set non-blocking mode

    def send(self, cmd):
        cmd = cmd.rstrip(self.LINE_TERMINATOR) + self.LINE_TERMINATOR
        send_data = bytes(cmd, 'ascii')
        logger.debug('sending: {}'.format(repr(send_data)))
        self.s.send(send_data)
        time.sleep(self.WAIT_AFTER_SEND)

    def receive(self, timeout=0.2):
        ready = select.select([self.s], [], [], timeout)
        if not ready[0]:
            raise MarantzTimeoutException('Not ready to read data in the specified timeout time {} s'.format(timeout))
        data = self.s.recv(self.BUFFER_SIZE)
        logger.debug('received: {}'.format(repr(data)))
        data = data.decode('ascii').strip(self.LINE_TERMINATOR)
        return [line.strip() for line in data.split(self.LINE_TERMINATOR)]

    @property
    def power(self):
        self.send('PW?')
        answer = self.receive()
        assert any(state in answer for state in ('PWON', 'PWSTANDBY'))
        return answer == 'PWON'

class MarantzException(Exception): pass
class MarantzTimeoutException(MarantzException): pass


def main():
    sc = cli.SR5009_CLI()
    args = sc.parse()
    s = SR5009(args.hostname)
    print("The receiver is {}.".format('on' if s.power else 'off'))

if __name__ == "__main__":
    main()
