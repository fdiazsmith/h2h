from pulsesensor import Pulsesensor
import time
import board    # For neopixel
import neopixel # neopixel

p = Pulsesensor()
p.startAsyncBPM()


pixels = neopixel.NeoPixel(board.D18, 8)



def loop():
    bpm = p.BPM
    if bpm > 0:
        print("BPM: %d" % bpm)
        pixels.fill(( int((p.rawSignal/65535)*100),22,10))
        pixels.show()
    else:
        print("No Heartbeat found", p.rawSignal)
    # time.sleep(1)

def exit():
    p.stopAsyncBPM()
    print("\n\tAdios mi corazon\n")



################################################################################
try:
    while True:
        loop()                  # Loop will run forever
#If keyboard Interrupt (CTRL-C) is pressed
except KeyboardInterrupt:
    exit()
    pass        # Go to next line
