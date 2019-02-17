/*
  Heart.h - Library for flashing Heart code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/
#ifndef Heart_h
#define Heart_h

#include "Smooth.h"
#include "Arduino.h"

class Heart
{
  public:
    Heart(int pin);
    float getBeat();
    int getRaw();
    bool beatDetected();
    float normal;
    Smooth m;
    Smooth signalCheck;

  private:
    int _pin;
    int _val;
    int _beat;
    int _max = 0;
    int _min = 1023;
    int _lastVal;

    int numReadings = 10;


    int readings[10];      // the readings from the analog input
    int readIndex = 0;              // the index of the current reading
    int total = 0;                  // the running total
    int average = 0;                // the average

    int beatsDetected[10];      // the readings from the analog input
    int bDreadIndex = 0;              // the index of the current reading
    int bDtotal = 0;                  // the running total
    int bDaverage = 0;

    void read();

    void smoothX();
};

#endif
