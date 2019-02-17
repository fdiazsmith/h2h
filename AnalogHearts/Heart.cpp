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

}

float Heart::getBeat(){
  read();
  smoothX();
  bool bb = beatDetected();

  normal = constrain((float)( _beat - _min ) / (float)( _max - _min ), 0,1);

  if(SERIAL_PRINT){
    Serial.print("HR  ");
    Serial.print( bb );
    Serial.print("\traw  ");
    Serial.print(_val);
    Serial.print("    ===smooth  ");
    Serial.print(normal);
    Serial.print("\tmax ");
    Serial.print(maxRA);
    Serial.print("\tmin ");
    Serial.println(minRA);
  }

  _lastVal = _val;
  float out;
  if(normal<0.5){
    out = normal*.25;
  }else{
    out = normal;
  }

  return normal;
}

void Heart::read(){
  _val = analogRead( _pin );
  // _val = (afv * (long)analogRead( _pin ) + (POWER - afv) * _val )/ POWER;
  if( beatDetected() ) {
    maxRA--;
    minRA++;
    // record the maximum sensor value
    if (_val > maxRA) {
      // _max = _val;
      maxRA = (alpha * _val + (POWER - alpha) * maxRA )/ POWER;
    }

    // record the minimum sensor value
    if (_val < minRA) {
      // _min = _val;
      minRA = (alpha * _val + (POWER - alpha) * minRA )/ POWER;
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

  return signalCheck.getSum() >= 7;
}

void Heart::smoothX(){
  m.add(_val);
  _beat = m.getAverage();
}
