#!/usr/bin/env python3

import time
import argparse
import random
import time
import board
import neopixel
import copy
import RPi.GPIO as GPIO     # Importing RPi library to use the GPIO pins

from pulsesensor import Pulsesensor
from pythonosc import osc_message_builder
from pythonosc import osc_bundle_builder
from pythonosc import udp_client


## set up OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="10.222.201.220", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()
# client = udp_client.SimpleUDPClient(args.ip, args.port)
client = udp_client.UDPClient(args.ip, args.port)


# msg.add_arg(4.0)
# # Add 4 messages in the bundle, each with more arguments.
# bundle.add_content(msg.build())
# print("\n\nargs\n", bundle.add_content)
# print("\n\n")



# bundle = bundle.build()
# You can now send it via a client as described in other examples.


## set up pulse sensor
p = Pulsesensor()
p.startAsyncBPM()

## setup neo pixels
pixels = neopixel.NeoPixel(board.D18, 8)
## Regular led
led_pin = 21            # Initializing the GPIO pin 21 for LED
hrm_pin = 26

GPIO.setmode(GPIO.BCM)          # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)   # Declaring pin 21 as output pin

GPIO.setup(hrm_pin, GPIO.IN)

pwm = GPIO.PWM(led_pin, 100)    # Created a PWM object
pwm.start(0)
###

START_TIME = time.time()
slowPrint = True
printInterval = 3


redX = 0
minRA = 0
def loop():
    global slowPrint
    global redX
    global minRA


    runtime = (time.time() - START_TIME);
    alpha = 255
    POWER = 255

    # client.send_message("/hrm", random.random() )
        # time.sleep(.33)
    bpm = p.BPM
    if bpm > 0:
        bundle = osc_bundle_builder.OscBundleBuilder(osc_bundle_builder.IMMEDIATELY)
        msg = osc_message_builder.OscMessageBuilder(address="/hrm")

        msg.add_arg(p.normal)
        bundle.add_content(msg.build())
        msg.add_arg(p.ampMin)
        bundle.add_content(msg.build())
        msg.add_arg(p.led)
        bundle.add_content(msg.build())
        msg.add_arg(p.longAverage)
        bundle.add_content(msg.build())

        client.send(bundle.build())

        pixels.fill((int(p.led*255),0,0))
        pixels.show()

        # print("normal: ", p.normal, "  longAverage: ", p.longAverage)
        # if runtime%1 <= 0.1 and slowPrint:
        #     slowPrint = False
        #     print("BPM: %d " % bpm )
        # elif runtime%1 > 0.1:
        #     slowPrint = True

    else:
        if runtime%printInterval <= 0.1 and slowPrint:
            slowPrint = False
            print("No Heartbeat found")
        elif runtime%printInterval > 0.1:
            slowPrint = True

def exit():
    print("\n\n\n<3 Adios Corazon\n")
    pixels.fill((0,0,0))
    pixels.show()
    p.stopAsyncBPM()

def map( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

def dump(obj):
   for attr in dir(obj):
       if hasattr( obj, attr ):
           print( "obj.%s = %s" % (attr, getattr(obj, attr)))

################################################################################
if __name__ == "__main__":
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        exit()
        pass


"""
        |\    /|
        | \  / |
   _____|__\/__|____
   |    |  /\  |    |
   |    | /  \ |    |
   |    | \  / |    |
   |____|__\/__|____|
        |  /\  |
        | /  \ |
        |/    \|


"""
