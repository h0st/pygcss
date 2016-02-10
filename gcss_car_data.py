#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid
import sys
import getopt

from M3Utility.RDFGraphGenerator import *
# from Utility.SubscriptionPerformanceTest import *
# from Utility.ProtectionPerformanceTest import *
from M3Utility.Utility import SmartSpaceData
# from Utility.StringPerformanceTest import *
from time import sleep
from M3Core.m3_kp import *

import os


#foaf http://xmlns.com/foaf/spec/index.rdf
#scribo http://cs.karelia.ru#

#if __name__ == "__main__":

node = KP("TestExample")
#ss_handle = ("X", (TCPConnector, ("192.168.112.104", 10010)))
ss_handle = ("X", (TCPConnector, ("127.0.0.1", 10010)))

if not node.join(ss_handle):
    sys.exit('Could not join to Smart Space')

node.leave(ss_handle)

    # connect to smart space
    #smart_space = SmartSpaceData()
    #smart_space.setSmartSpaceName("X")
    # smart_space.setIPADDR("localhost")
    # smart_space.setPort(10010)

    # join
    #smart_space.joinSpace()




#
# TODO: menu with SWITCH as in mdbci!
#
'''
def main(argv: None):

    try:
        opts, args = getopt(sys.argv[1:], "h", "[help]")
    except getopt.error as msg:
        print(msg)
        print("for Help using --help")
        sys.exit(2)
    #
    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
    # analyse
    for arg in args:
        print("Hello!")
        # process(arg) # process in other place

if __name__ == "__main__":
    main("-h")
'''
