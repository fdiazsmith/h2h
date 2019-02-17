


/*
  Smooth.cpp
*/

#include "Smooth.h"
#include "Arduino.h"

Smooth::Smooth( ){
  numReadings = 10;
}
Smooth::Smooth(int n = 10){
  numReadings = n;
}

void Smooth::add(int a){
  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor:
  readings[readIndex] = a;
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= numReadings) {
    // ...wrap around to the beginning:
    readIndex = 0;
  }
}

int Smooth::getSum(){
  return total;
}
int Smooth::getAverage(){
  return total / numReadings;;
}
