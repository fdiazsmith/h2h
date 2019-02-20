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


def loop():
        # time.sleep(1)
    bpm = p.BPM
    if bpm > 0:
        client.send_message("/hrm", p.rawSignal )
        print("Signal: %d" % p.rawSignal)
        pixels.fill((20,22,10))
        pixels.show()
    else:
        print("No Heartbeat found")
        time.sleep(1)

def exit():
    print("\nAdios Coraznn\n")
    p.stopAsyncBPM()


################################################################################
if __name__ == "__main__":
    try:
        while True:
            loop()
    except:
        exit()
        pass
