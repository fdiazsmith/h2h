/*
  Analog Input

  Demonstrates analog input by reading an analog sensor on analog pin 0 and
  turning on and off a light emitting diode(LED) connected to digital pin 13.
  The amount of time the LED will be on and off depends on the value obtained
  by analogRead().

  The circuit:
  - potentiometer
    center pin of the potentiometer to the analog input 0
    one side pin (either one) to ground
    the other side pin to +5V
  - LED
    anode (long leg) attached to digital output 13
    cathode (short leg) attached to ground

  - Note: because most Arduinos have a built-in LED attached to pin 13 on the
    board, the LED is optional.

  created by David Cuartielles
  modified 30 Aug 2011
  By Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/AnalogInput
*/
#include "Heart.h"
// #include "Smooth.h"

const int ledPin = 3;      // select the pin for the LED
int ledValue = 0;

Heart h1(A0);
Heart h2(A1);

// Smooth sm((int)10);

void setup() {
  // declare the ledPin as an OUTPUT:
  pinMode(ledPin, OUTPUT);

  Serial.begin(9600);
  Serial.println("Analog Heart!");
}

void loop() {

  float h1V = 1- h1.getBeat();
   float h2V = 1;
   // sm.add(h1V);
  // float h2V = 1- h2.getBeat();
  ledValue = (h1V*h2V) * 255;
  // Serial.println(h1V);
  // Serial.print("  |  ");
  // Serial.print(h1V);
  // Serial.print(",");
  // Serial.print(h1.getRaw());
  // Serial.print(",");
  Serial.println(h1.getRaw());
  analogWrite(ledPin, ledValue);


}
