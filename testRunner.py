#!/usr/bin/python
# coding: utf8
from tools import *


if __name__ == '__main__':
    tests = loadTests()

    for test in tests:
        if test['type'] == "ping":
            testPing(test)

        elif test['type'] == "mongo":
            testMongo(test)

        elif test['type'] == "curl":
            testCurl(test)

        elif test['type'] == "port":
            testPort(test)
