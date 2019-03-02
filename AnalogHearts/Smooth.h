

/*
  Smooth.h
*/
#ifndef Smooth_h
#define Smooth_h

#include "Arduino.h"

class Smooth{
  public:
    Smooth( );
    Smooth( int n );

    void add(int a);
    int getSum();
    int getAverage();
    bool SERIAL_PRINT = false;

  private:
    int numReadings;
    // find how to instantiate this array with different numbers
    int readings[10];               // the readings from the analog input
    int readIndex = 0;              // the index of the current reading
    int total = 0;                  // the running total
    int average = 0;                // the average

};

#endif
