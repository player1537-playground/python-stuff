#!/usr/bin/python

import sys

with open(argv[1], "r") as f:
    lines = f.readlines()
    for line in lines:
        for c in line:
            print "%s\n" % c

