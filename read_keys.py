###################################
# Smart keycode-ecode mapper by CRImier
###################################

import sys

#Preparations:
print "This script lets you make a keycode-ecode mapping from, say, a serial stream, automating all the recording and suggesting ecodes for you."
print "Quick disambiguation - keycode is some kind of a number/char/string, and ecode is a string that can be input into Linux uinput system to produce a keypress. For example, 'KEY_LEFT' or 'KEY_A' is a ecode, but 0x87, 'a' or 'Left button' would be a keycode."
print "Once you've got a serial-connected keyboard that has around 100 keys and no driver, you'll learn to use that function."
print "To suit this script to your needs, open it in your text editor to find instructions."

print "This script listens for keycodes and, once detected, lets you choose the appropriate ecode from system-wide ecode collection"
print "Once Ctrl+C-ed, it prints out a Python dictionary of keycode:ecode entries and exits"

#Here are your instructions.

#########################
#This is the place where you import your driver module that can actually communicate to your device.
#Say, you've got a serial stream of chars coming from a device that you want to make a driver for. 
#This utility will need to detect those chars, so your job is to write a driver that can call a function once a keycode is received (those kind of functions are called callbacks)
#For an example, see https://github.com/CRImier/ChatpadDriver - there's read_keys.py which was the first version of this utility, so it's mostly the same.
#Oh, and it's a serial driver example =)

#from driver import MyCoolDevice

#########################

d = {} #Yes, this is THE dictionary.

print " "
print "This script uses Python 'evdev' module ecodes.ecodes.keys() list as a ecode base"
print "Run evdev-install.sh to install it (uses apt-get and pip as a package manager)"
from evdev.ecodes import ecodes
ecodes = [key for key in ecodes.keys() if key.startswith("KEY_")] #filtered ecodes 
fsecodes = [key[4:] for key in ecodes] #filtered and stripped ecodes

print " "
print "#########################"
print "-How to choose a proper ecode?"
print "-This script takes all KEY_$ ecodes and wait you to either enter the $ or search for an ecode."
print "To enter the $, enter it in uppercase (i.e. 'A' would mean that you chose 'KEY_A')."
print "To search for an ecode, enter part of it in lowercase. Space-separated $ containing your input symbols will be printed out."
print "#########################"
print " "

#########################
#The callback function is designed to take multiple arguments, first being a list of keycodes of buttons that are pressed (it doesn't care about all the other arguments)
#It takes only the first element of the list, however.
########################

def callback(pressed, *args):
    if not pressed or len(pressed) > 1:
        return None
    print "Keypress detected!"
    keycode = pressed[0]
    try:
        while True:
            if keycode in d.keys():
                print "This key has already been pressed, beware"
            user_input = raw_input("Enter or search:").strip(" ")
            if not user_input: 
                return None
            if not user_input.islower() and not user_input.isupper() and not user_input.isdigit():
                print "Mixed case input detected, ABORT ABORT"
                continue
            elif user_input.isupper() or user_input.isdigit():
                if user_input in fsecodes:
                    if 'KEY_'+user_input in d.values(): print "Value already there, overwriting"
                    d[keycode] = 'KEY_'+user_input
                    print "Key KEY_"+user_input+" saved"
                    return True #Exiting as we've recorded the keycode successfully.
                else:
                    print "Ecode not found, try again"
                    continue
            elif user_input.islower():
                user_input = user_input.upper()
                suggestions = [key for key in fsecodes if user_input in key]
                if suggestions:
                    print " ".join(suggestions)
                else:
                    print "Sorry, nothing found."
    except KeyboardInterrupt:
        return None
    #Once you've successfully recorded one key, there's immediately a 'Keypress detected!' and a key prompt?
    #Must be you pressing a key while it was running, so it got to the serial buffer and was afterwards immediately processed by your driver
    #Alternatively, you need to debug your driver better to avoid ghost keypress detection (i.e. an Xbox Chatpad sends a keycode 4 times.)
    #You could also flush a serial buffer of your driver at the start of this callback - this would be a hack though.

def exit():
    print d
    sys.exit(0)    

#Now is the actual key listening
print "Starting listening."
print "If you accidentally press more than one key or an unneeded key and don't need to register it, just send an empty response."
print " "

###########################
# Put your init function here, for example, creating an object from your driver
# Set a callback if it's needed - or write your own event loop

#device = MyCoolDevice(callback=my_callback)

###########################

try:
    #######################
    # Put your event loop function call here - or write a simple polling event loop, whatever.
    
    pass 
    #device.listen()
    
    #######################
except KeyboardInterrupt:
    exit()
