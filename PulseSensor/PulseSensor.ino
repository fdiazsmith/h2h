
#define USE_ARDUINO_INTERRUPTS true
#include <PulseSensorPlayground.h>

const int OUTPUT_TYPE = SERIAL_PLOTTER;

const int PULSE_SENSOR_COUNT = 2;

const int PULSE_INPUT0 = A0;
const int PULSE_BLINK0 = 13;    // Pin 13 is the on-board LED
const int PULSE_FADE0 = 5;

const int PULSE_INPUT1 = A1;
const int PULSE_BLINK1 = 12;
const int PULSE_FADE1 = 11;

const int THRESHOLD = 550;   // Adjust this number to avoid noise when idle

int led = 3;
double normals[2];
double es[2];
long sofB[2];
long currentTime;


PulseSensorPlayground pulseSensor(PULSE_SENSOR_COUNT);

void setup() {

  Serial.begin(250000);


  pulseSensor.analogInput(PULSE_INPUT0, 0);
  pulseSensor.blinkOnPulse(PULSE_BLINK0, 0);
  pulseSensor.fadeOnPulse(PULSE_FADE0, 0);

  pulseSensor.analogInput(PULSE_INPUT1, 1);
  pulseSensor.blinkOnPulse(PULSE_BLINK1, 1);
  pulseSensor.fadeOnPulse(PULSE_FADE1, 1);

//  pulseSensor.setSerial(Serial);
  pulseSensor.setOutputType(OUTPUT_TYPE);
  pulseSensor.setThreshold(THRESHOLD);

  pinMode(led, OUTPUT);
  for (int i = 0; i < PULSE_SENSOR_COUNT; i++) {
    normals[i] = 0.0;
  }
  // Now that everything is ready, start reading the PulseSensor signal.
  if (!pulseSensor.begin()) {
    /*
       PulseSensor initialization failed,
       likely because our Arduino platform interrupts
       aren't supported yet.

       If your Sketch hangs here, try changing USE_ARDUINO_INTERRUPTS to false.
    */
    for (;;) {
      // Flash the led to show things didn't work.
      digitalWrite(PULSE_BLINK0, LOW);
      delay(50);
      digitalWrite(PULSE_BLINK0, HIGH);
      delay(50);
    }
  }
}

void loop() {


  delay(20);

  // write the latest sample to Serial.
  // pulseSensor.outputSample();

  /*
     If a beat has happened on a given PulseSensor
     since we last checked, write the per-beat information
     about that PulseSensor to Serial.
  */
  for (int i = 0; i < PULSE_SENSOR_COUNT; ++i) {
    if (pulseSensor.sawStartOfBeat(i)) {
      // pulseSensor.outputBeat(i);
//      pulseSensor.getLatestSample(i);
//      pulseSensor.getPulseAmplitude(i);
    sofB[i] = millis();
    }
    // normals[i] = constrain( (float)(pulseSensor.getLatestSample(i) - pulseSensor.getPulseAmplitude(i)) / (float) pulseSensor.getPulseAmplitude(i), 0, 1 );
    normals[i] = pulseSensor.fadeLevel(i)/255.0;
    // es[i] =easeInQuad( normals[i], 0, 1, pulseSensor.getInterBeatIntervalMs(i) );

  }
  // pulseSensor.getLastBeatTime(i);
  // pulseSesnor.getInterBeatIntervalMs(i);

  analogWrite(led, (normals[0] * normals[1])*255 );

  Serial.println( pulseSensor.fadeLevel(0)/255.0 );

  Serial.print(normals[0]);
  Serial.print(",");
  Serial.print(normals[1]);
  Serial.print(",");
  Serial.println(normals[0] * normals[1]);

}


//t current time
// b start value;
// c change in value
// duration
// double easeInQuad (long t, double b, double c, int d) {
//   t /= d;
//   return c*t*t + b;
// }

// quadratic easing in - accelerating from zero velocity
// t: current time, b: beginning value, c: change in value, d: duration
// t and d can be in frames or seconds/milliseconds
float easeInQuad (float t, float b, float c, float d) {
	return c*(t/=d)*t + b;
}
