#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid

from M3Utility.RDFGraphGenerator import *
# from Utility.SubscriptionPerformanceTest import *
# from Utility.ProtectionPerformanceTest import *
from M3Utility.Utility import SmartSpaceData
# from Utility.StringPerformanceTest import *
from time import sleep
from M3Core.m3_kp import *

import sys, os, getopt


#foaf http://xmlns.com/foaf/spec/index.rdf

# Menu actions list
menu_actions = {}

#
# Main menu functions
#
def main_menu():
    os.system('clear')

    print 'Welcome to GCSS CLI tool'
    print 'Please choose one menu point or use command line parameters'
    print '1. Menu 1'
    print '2. Menu 2'
    print '\n0. Quit'
    choise = raw_input(" >> ")
    exec_menu(choise)

# execute menu
def exec_menu(choise):
    os.system('clear')
    ch = choise.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, try again.\n"
            menu_actions['main_menu']()
    return

# test menus
def menu1():
    print 'Hello, its a menu 1\n'
    print '9. Back'
    print '0. Quit'
    choise = raw_input(" >> ")
    exec_menu(choise)
    return

def menu2():
    print 'Hello, its a menu 2\n'
    print '9. Back'
    print '0. Quit'
    choise = raw_input(" >> ")
    exec_menu(choise)
    return

def back():
    menu_actions['main_menu']()

def exit():
    sys.exit()

#
# Menu Actions List
#
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit
}

#
# Command line parameters
def cli_menu(argv):
    # file = ''
    try:
        opts, args = getopt.getopt(argv, "hiallalor", "[help]")
    except getopt.GetoptError as msg:
        print(msg)
        print("for Help using --help")
        sys.exit(2)
    #
    for opt, arg in opts:
        # TODO change to switch
        if opt in ("-h", "--help"):
            print('... HELP ...')
            sys.exit(0)
        elif opt in ("-i", "--hello"):
            print("Hello!")
        elif opt in ("-al", "--alt"):
            alt = arg
            print("Altitude: "+alt)
        elif opt in ("-la", "--lat"):
            lat = arg
            print("Latitude: "+lat)
        elif opt in ("-lo", "--lon"):
            lon = arg
            print("Longitude: "+lon)
        elif opt in ("-r", "--radius"):
            radius = arg
            print("Radius: "+radius)


#
# MAIN
#
if __name__ == "__main__":

    cli_menu(sys.argv[1:])
    #main_menu()