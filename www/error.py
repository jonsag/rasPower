#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

import sys

# handle errors


def onError(errorCode, extra):
    print("\nError:")
    if errorCode in (1, 2):  # print error information, print usage and exit
        print(extra)
        usage(errorCode)
    elif errorCode == 3:  # print error information and exit
        print(extra)
        sys.exit(errorCode)
    elif errorCode == 4:  # print error information and return running program
        print(extra)
        return

# print usage information


def usage(exitCode):
    print("\nUsage:")
    print("----------------------------------------")
    print("%s " % sys.argv[0])

    print("\n%s -v" % sys.argv[0])
    print("    Verbose output")

    print("\n%s -h" % sys.argv[0])
    print("    Show help")

    sys.exit(exitCode)
