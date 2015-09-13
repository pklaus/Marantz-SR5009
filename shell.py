#!/usr/bin/env python

import argparse
import atexit
import os
import readline
import logging

from sr5009 import SR5009, MarantzTimeoutException

try:
    input = input
except:
    input = raw_input

def loglevel(string):
    string = string.upper()
    loglevels = set(('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'))
    for level in loglevels:
        if level.startswith(string):
            return level
    raise argparse.ArgumentTypeError('Invalid loglevel, choose from {}'.format(loglevels))

def main():
    parser = argparse.ArgumentParser(description='SR5009 CLI')
    parser.add_argument('--loglevel', type=loglevel, default='INFO', help='Set the loglevel of this software')
    parser.add_argument('hostname', help='The hostname of the SR5009')

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)

    histfile = os.path.join(os.path.expanduser("~"), ".sr5009_history")
    try:
        readline.read_history_file(histfile)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)

    s = SR5009(args.hostname)
    print("The receiver is {}.".format('on' if s.power else 'off'))

    try:
        while True:
            line = input('SR5009> ')
            if not line: continue
            if line.startswith('quit'): break
            line = line.strip()
            s.send(line)
            if '?' in line:
                answers = []
                try:
                    answers = s.receive()
                except MarantzTimeoutException:
                    print('No answer in time.')
                if len(answers) == 1:
                    print(answers[0])
                elif len(answers) > 1:
                    print('\n'.join(answers))
    except (EOFError, KeyboardInterrupt):
        print()

if __name__ == "__main__":
    main()

