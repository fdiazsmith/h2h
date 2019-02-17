/*
  Heart.h - Library for flashing Heart code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/
#ifndef Heart_h
#define Heart_h

#include "Smooth.h"
#include "Arduino.h"

#define POWER 256

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

    long alpha = 254;
    long maxRA = 0;
    long minRA = 1023;
    long foo;


  private:
    int _pin;
    long _val;
    long _beat;
    long _max = 0;
    long _min = 1023;
    long _lastVal;

    int numReadings = 10;


    void read();

    void smoothX();
};

#endif
