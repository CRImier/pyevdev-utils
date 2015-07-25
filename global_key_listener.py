#!/usr/bin/env python
from evdev import InputDevice, list_devices, categorize, ecodes
import threading

def listen_for_events(dev):
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            print dev.name+" - "+dev.fn+":  "+str(categorize(event))

print "This script grabs all the devices and doesn't allow keystrokes to pass through normally, effectively blocking you all the ways to stop this script by keyboard you're using (not mouse, thankfully)."
#TODO:Add a device selection to excluse one device that could to the Ctrl+C
raw_input("Press Enter to continue or Ctrl+C to exit")
devices = [InputDevice(fn) for fn in list_devices()]
for dev in devices:
    print(dev.fn, dev.name, dev.phys)
    thread = threading.Thread(target=listen_for_events, args=(dev,))
    thread.daemon = False
    thread.start()
