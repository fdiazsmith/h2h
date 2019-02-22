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
        # time.sleep(1)
    bpm = p.BPM
    if bpm > 0:
        sendHRM = (p.normal - 0.43)*4
        # sendHRM = map(p.normal, p.ampMin, p.ampMax, 0.1, .9)
        # copyhrm = copy.deepcopy(sendHRM)
        redX = int(map(sendHRM,0,1,0,100))
        minRA = (alpha * redX + (POWER - alpha) * minRA )/ POWER;
        if redX < 0:
            redX = 0
        elif redX > 100:
            redX = 100;

        # pixels.fill((redX,0,0))
        # pixels.show()
        pwm.ChangeDutyCycle(minRA)
        client.send_message("/hrm", minRA/255 )
        print("BPM: %d " % bpm , "Normal: ", minRA/255 )

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
