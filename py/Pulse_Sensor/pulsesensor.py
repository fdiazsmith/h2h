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
        self.ampMin = 0
        self.normal = 0
        self.thresh = 0
        self.led = 0
        # self.adc = MCP3008(bus, device)


        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)

        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0
        self.chan = AnalogIn(mcp, MCP.P7)

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

        longAverage = Averager(1000)
        shortAverage = Averager(20)
        minAverage = Averager(20)
        maxAverage = Averager(20)

        while not self.thread.stopped:
            # self.rawSignal = self.adc.read(self.channel)
            self.rawSignal = self.chan.value
            self.normal = self.rawSignal/FULL_ANALOG_INPUT
            # self.calcAverage()                        # only calculate average when we have a beat
            longAverage.add(self.normal)
            self.longAverage = longAverage.getAvrg()

            shortAverage.add(self.normal)
            self.setLed(shortAverage.getAvrg())
            # self.led = shortAverage.getAvrg()
            currentTime = int(time.time()*1000)

            sampleCounter += currentTime - lastTime
            lastTime = currentTime

            N = sampleCounter - lastBeatTime

            # find the peak and trough of the pulse wave
            if self.rawSignal < self.thresh and N > (IBI/5.0)*3:     # avoid dichrotic noise by waiting 3/5 of last IBI
                # print("avoiding noise", self.rawSignal, N )
                if self.rawSignal < T:                          # T is the trough
                    T = self.rawSignal                          # keep track of lowest point in pulse wave
                    minAverage.add(T/FULL_ANALOG_INPUT)
                    self.ampMin = minAverage.getAvrg()

            if self.rawSignal > self.thresh and self.rawSignal > P:
                P = self.rawSignal
                maxAverage.add(P/FULL_ANALOG_INPUT)
                self.ampMax = maxAverage.getAvrg()

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
                self.ampNormal = amp/FULL_ANALOG_INPUT      # get amplitude of the pulse wave
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

    def setLed(self, val):
        _led = (val - self.ampMin) * 4

        if _led < 0:
            _led = 0
        elif _led > 1:
            _led = 1

        self.led = _led


    def map( x,  in_min,  in_max,  out_min,  out_max):
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;



class Averager:
    def __init__(self, size = 10, initVal = 0):
        self.__size = size
        self.__avrg = [initVal] * self.__size    # keep a long running avrg
        self.__readIndex = 0        # start of the averaging index
        self.avrgTotal = 0
        # print("\n\t Averager size: %d \n" % self.__size)

    def add(self, value , debug = False ):
        self.avrgTotal = self.avrgTotal - self.__avrg[self.__readIndex]

        self.__avrg[self.__readIndex] = value

        self.avrgTotal = self.avrgTotal + self.__avrg[self.__readIndex]

        self.__readIndex += 1

        if self.__readIndex >= self.__size:
            self.__readIndex = 0

        # self.longAverage = self.avrgTotal / self.__size
        if debug:
            print("size: ", self.__size, "  index: ", self.__readIndex,  "   self.avrgTotal: ",self.avrgTotal,   "  average: ", self.longAverage)

    def getAvrg(self) -> float:
        return self.avrgTotal / self.__size




"""
   *
   * @webref shape:curves
   * @param a coordinate of first point on the curve
   * @param b coordinate of first control point
   * @param c coordinate of second control point
   * @param d coordinate of second point on the curve
   * @param t value between 0 and 1
   * @see PGraphics#bezier(float, float, float, float, float, float, float, float, float, float, float, float)
   * @see PGraphics#bezierVertex(float, float, float, float, float, float)
   * @see PGraphics#curvePoint(float, float, float, float, float)
   */
  public float bezierPoint(float a, float b, float c, float d, float t) {
    float t1 = 1.0f - t;
    return (a*t1 + 3*b*t)*t1*t1 + (3*c*t1 + d*t)*t*t;
}
"""
