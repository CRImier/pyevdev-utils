###################################
# Ecode search by CRImier
###################################

import sys 

#Preparations:

print " "
print "#########################"
print "-This script takes all KEY_$ ecodes and lets you search among them. To search for an ecode, enter part of it. Space-separated $ containing your input symbols will be printed out."
print "#########################"
print " "

try:
    from evdev.ecodes import ecodes
except:
    print "This script uses Python 'evdev' module ecodes.ecodes.keys() list as a ecode base"
    print "Run evdev-install.sh to install it (uses apt-get and pip as a package manager)"
    sys.exit(0)

ecodes = [key for key in ecodes.keys() if key.startswith("KEY_")] #filtered ecodes 
fsecodes = [key[4:] for key in ecodes] #filtered and stripped ecodes

while True:
    user_input = raw_input("Enter or search:").strip(" ")
    if not user_input: 
        continue
    user_input = user_input.upper()
    suggestions = [key for key in fsecodes if user_input in key]
    if suggestions:
        print " ".join(suggestions)
    else:
        print "Sorry, nothing found."
