import time
import argparse
import random
import time
import board
import neopixel

from pulsesensor import Pulsesensor
from pythonosc import osc_message_builder
from pythonosc import udp_client


## set up OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="172.20.10.4", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

## set up pulse sensor
p = Pulsesensor()
p.startAsyncBPM()

## setup neo pixels
pixels = neopixel.NeoPixel(board.D18, 11)

START_TIME = time.time()
slowPrint = True
printInterval = 3
"""
-[x] ocs sendign
-[ ] neo pixel
-[ ]

"""

def loop():
    global slowPrint
    runtime = (time.time() - START_TIME);



    # client.send_message("/hrm", random.random() )
        # time.sleep(1)
    bpm = p.BPM
    if bpm > 0:
        client.send_message("/hrm", p.normal )
        # print("BPM: %d" % bpm)
        # pixels.fill((20,22,10))
        # pixels.show()
    else:
        if runtime%printInterval <= 0.1 and slowPrint:
            slowPrint = False
            print("No Heartbeat found")
        elif runtime%printInterval > 0.1:
            slowPrint = True

def exit():
    print("\nAdios Corazon\n")
    p.stopAsyncBPM()


################################################################################
if __name__ == "__main__":
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        exit()
        pass
