/*
  Heart.cpp - Library for flashing Heart code.
  Created by David A. Mellis, November 2, 2007.
  Released into the public domain.
*/

#include "Arduino.h"
#include "Heart.h"

Heart::Heart(int pin){
  pinMode(pin, INPUT);
  _pin = pin;

  for (int thisReading = 0; thisReading < numReadings; thisReading++) {
    readings[thisReading] = 0;
  }
}

float Heart::getBeat(){
  read();
  smoothX();
  bool bb = beatDetected();

  normal = constrain((float)( _beat - _min ) / (float)( _max - _min ), 0,1);
  // normal = constrain((float)( _beat - 460 ) / (float)( 550 - 460 ), 0,1);
  Serial.print("signal check   ");
  Serial.print( signalCheck.getSum() );
  Serial.print("HR  ");
  Serial.print( bb );
  Serial.print("   ==raw  ");
  Serial.print(_val);
  Serial.print("    ===smooth  ");
  Serial.print(normal);
  Serial.print("     max ");
  Serial.print(_max);
  Serial.print("     min ");
  Serial.println(_min);

  _lastVal = _val;
  return normal;
}

void Heart::read(){
  _val = analogRead( _pin );
  if( beatDetected() ) {
    // record the maximum sensor value
    if (_val > _max) {
      _max = _val;
    }

    // record the minimum sensor value
    if (_val < _min) {
      _min = _val;
    }
  }

}
int Heart::getRaw(){
  return _val;
}

bool Heart::beatDetected(){
  bool b = false;
  if( abs( _lastVal - _val) > 50
      ||  _lastVal == _val
      || _val == 0
    ){
    b = false;
  }
  else{
    b = true;
  }
  signalCheck.add(b);
  // // subtract the last reading:
  // bDtotal = bDtotal - beatsDetected[bDreadIndex];
  // // read from the sensor:
  // beatsDetected[bDreadIndex] = b;
  // // add the reading to the total:
  // bDtotal = bDtotal + beatsDetected[bDreadIndex];
  // // advance to the next position in the array:
  // bDreadIndex = bDreadIndex + 1;
  //
  // // if we're at the end of the array...
  // if (bDreadIndex >= 10) {
  //   // ...wrap around to the beginning:
  //   bDreadIndex = 0;
  // }
  return signalCheck.getSum() == 10;
}

void Heart::smoothX(){
  m.add(_val);
  _beat = m.getAverage();
  //
  // morse.dot();
  // morse.dash();
  // // subtract the last reading:
  // total = total - readings[readIndex];
  // // read from the sensor:
  // readings[readIndex] = _val;
  // // add the reading to the total:
  // total = total + readings[readIndex];
  // // advance to the next position in the array:
  // readIndex = readIndex + 1;
  //
  // // if we're at the end of the array...
  // if (readIndex >= numReadings) {
  //   // ...wrap around to the beginning:
  //   readIndex = 0;
  // }
  //
  // // calculate the average:
  // // average = total / numReadings;
  // _beat = total / numReadings;
}
