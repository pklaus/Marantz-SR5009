#!/usr/bin/env python

import argparse

class SR5009_CLI(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='SR5009 CLI')
        self.parser.add_argument('hostname', help='The hostname of the SR5009')
        
    def parse(self):
        self.args = self.parser.parse_args()
        return self.args

if __name__ == "__main__":
    sc = SR5009_CLI()
    sc.parse()
    from pprint import pprint
    pprint(sc.args.__dict__)

