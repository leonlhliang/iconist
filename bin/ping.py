#!/usr/bin/env python
import sys
import requests

SCRIPT, HOST = sys.argv

header = requests.get(HOST).headers
keys = list(header.keys())
keys.sort(key=len, reverse=True)
length = len(keys[0])

for key in keys:
    padded = key
    for count in range(0, length - len(key)):
        padded = " " + padded
    print "%s: %s" % (padded, header[key])


sys.exit(0)
