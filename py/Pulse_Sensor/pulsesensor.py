# extended from https://github.com/WorldFamousElectronics/PulseSensor_Amped_Arduino

import time
import threading
# from MCP3008 import MCP3008
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

FULL_ANALOG_INPUT = 0xFFFF #65535 #1023 (0x3FF)
HALF_ANALOG_INPUT = 0x7FFF #512 (0x1FF)
TIME_THRESHOLD = 250
INITAIAL_AMP_RATIO = 10
THRESHOLD = 35000 #525

class Pulsesensor:
    def __init__(self, channel = 0, bus = 0, device = 0):
        self.channel = channel
        self.BPM = 0
        self.rawSignal = 0
        self.ampNormal = 0
        self.ampMax = 0
        self.ampMix = 0
        self.normal = 0
        self.avrg = [THRESHOLD/0xFFFF] * 1    # keep a long running avrg
        self.readIndex = 0        # start of the averaging index
        self.avrgTotal = 0
        self.thresh = 0
        # self.adc = MCP3008(bus, device)

        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan = AnalogIn(mcp, MCP.P0)

    def getBPMLoop(self):
        global HALF_ANALOG_INPUT
        global FULL_ANALOG_INPUT
        global INITAIAL_AMP_RATIO
        global TIME_THRESHOLD
        # init variables
        rate = [0] * 10         # array to hold last 10 IBI values
        sampleCounter = 0       # used to determine pulse timing
        lastBeatTime = 0        # used to find IBI
        P = HALF_ANALOG_INPUT                 # used to find peak in pulse wave, seeded
        T = HALF_ANALOG_INPUT                 # used to find trough in pulse wave, seeded
        self.thresh = THRESHOLD    #525        # used to find instant moment of heart beat, seeded
        amp = FULL_ANALOG_INPUT/ INITAIAL_AMP_RATIO              # used to hold amplitude of pulse waveform, seeded
        firstBeat = True        # used to seed rate array so we startup with reasonable BPM
        secondBeat = False      # used to seed rate array so we startup with reasonable BPM

        IBI = 600               # int that holds the time interval between beats! Must be seeded!
        Pulse = False           # "True" when User's live heartbeat is detected. "False" when not a "live beat".
        lastTime = int(time.time()*1000)


        while not self.thread.stopped:
            # self.rawSignal = self.adc.read(self.channel)
            self.rawSignal = self.chan.value
            self.normal = self.rawSignal/0xFFFF
            self.calcAverage()                  # only calculate average when we have a beat
            currentTime = int(time.time()*1000)

            sampleCounter += currentTime - lastTime
            lastTime = currentTime

            N = sampleCounter - lastBeatTime

            # find the peak and trough of the pulse wave
            if self.rawSignal < self.thresh and N > (IBI/5.0)*3:     # avoid dichrotic noise by waiting 3/5 of last IBI
                # print("avoiding noise", self.rawSignal, N )
                if self.rawSignal < T:                          # T is the trough
                    # print(" < T", T)
                    T = self.rawSignal                          # keep track of lowest point in pulse wave
                    self.ampMin = T/0xFFFF

            if self.rawSignal > self.thresh and self.rawSignal > P:
                # print("P>", P)
                P = self.rawSignal
                self.ampMax = P/0xFFFF
            # print("N", N)
            # signal surges up in value every time there is a pulse
            if N > TIME_THRESHOLD:                                 # avoid high frequency noise
                # print("N", N)
                if self.rawSignal > self.thresh and Pulse == False and N > (IBI/5.0)*3:

                    Pulse = True                        # set the Pulse flag when we think there is a pulse
                    IBI = sampleCounter - lastBeatTime  # measure time between beats in mS
                    lastBeatTime = sampleCounter        # keep track of time for next pulse

                    if secondBeat:                      # if this is the second beat, if secondBeat == TRUE
                        secondBeat = False;             # clear secondBeat flag
                        for i in range(len(rate)):      # seed the running total to get a realisitic BPM at startup
                          rate[i] = IBI

                    if firstBeat:                       # if it's the first time we found a beat, if firstBeat == TRUE
                        firstBeat = False;              # clear firstBeat flag
                        secondBeat = True;              # set the second beat flag
                        continue

                    # keep a running total of the last 10 IBI values
                    rate[:-1] = rate[1:]                # shift data in the rate array
                    rate[-1] = IBI                      # add the latest IBI to the rate array
                    runningTotal = sum(rate)            # add upp oldest IBI values

                    runningTotal /= len(rate)           # average the IBI values
                    self.BPM = 60000/runningTotal       # how many beats can fit into a minute? that's BPM!

            if self.rawSignal < self.thresh and Pulse == True:       # when the values are going down, the beat is over
                Pulse = False                           # reset the Pulse flag so we can do it again
                amp = P - T
                self.ampNormal = amp/0xFFFF      # get amplitude of the pulse wave
                self.thresh = amp/2 + T                # set self.thresh at 50% of the amplitude
                P = self.thresh                              # reset these for next time
                T = self.thresh

            if N > 2500:                                # if 2.5 seconds go by without a beat
                self.thresh = HALF_ANALOG_INPUT                            # set self.thresh default
                P = HALF_ANALOG_INPUT                                 # set P default
                T = HALF_ANALOG_INPUT                                 # set T default
                lastBeatTime = sampleCounter            # bring the lastBeatTime up to date
                firstBeat = True                        # set these to avoid noise
                secondBeat = False                      # when we get the heartbeat back
                self.BPM = 0

            time.sleep(0.005)


    # Start getBPMLoop routine which saves the BPM in its variable
    def startAsyncBPM(self):
        self.thread = threading.Thread(target=self.getBPMLoop)
        self.thread.stopped = False
        self.thread.start()
        return

    # Stop the routine
    def stopAsyncBPM(self):
        self.thread.stopped = True
        self.BPM = 0
        return

    def calcAverage(self):
        self.avrgTotal = self.avrgTotal - self.avrg[self.readIndex]

        self.avrg[self.readIndex] = self.normal

        self.avrgTotal = self.avrgTotal + self.avrg[self.readIndex]

        self.readIndex += 1

        if self.readIndex >= len(self.avrg):
            self.readIndex = 0

        self.average = self.avrgTotal / len(self.avrg)
