import time
import argparse
import random
import time
import board
import neopixel
import copy

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
pixels = neopixel.NeoPixel(board.D18, 8)

START_TIME = time.time()
slowPrint = True
printInterval = 3
"""
-[x] ocs sendign
-[ ] neo pixel
-[ ]

"""
redX = 0
def loop():
    global slowPrint
    global redX
    runtime = (time.time() - START_TIME);



    # client.send_message("/hrm", random.random() )
        # time.sleep(1)
    bpm = p.BPM
    if bpm > 0:
        sendHRM = map(p.normal, p.ampMin, p.ampMax, 0.1, .9)
        client.send_message("/hrm", p.normal )
        print("BPM: %d " % bpm , "Normal: ", p.normal )
        # copyhrm = copy.deepcopy(sendHRM)
        # redX = int(map(copyhrm,0,1,0,255))
        #
        # if redX < 0:
        #     redX = 0
        # elif redX > 255:
        #     redX = 255;
        #
        # pixels.fill((redX,5,5))
        # pixels.show()

    else:
        if runtime%printInterval <= 0.1 and slowPrint:
            slowPrint = False
            print("No Heartbeat found")
        elif runtime%printInterval > 0.1:
            slowPrint = True

def exit():
    print("\nAdios Corazon\n")
    pixels.fill((0,0,0))
    pixels.show()
    p.stopAsyncBPM()

def map( x,  in_min,  in_max,  out_min,  out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

################################################################################
if __name__ == "__main__":
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        exit()
        pass
