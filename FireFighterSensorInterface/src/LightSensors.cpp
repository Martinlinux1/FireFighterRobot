#include "LightSensors.h"

LightSensors::LightSensors(short *pins) {
  LightSensors::lightSensorPins = pins;

  analogReadResolution(8);

  for (int i = 0; i < arrLen(pins); i++) {
    pinMode(LightSensors::lightSensorPins[i], INPUT);
  }
}

int LightSensors::getLight(short sensor) {
  return map(analogRead(LightSensors::lightSensorPins[sensor]), 0, 1023, 0, 255);
}

// bool LightSensors::isLight(int *sensor, int treshold) {
//   for (int i = 0; i < arrLen(LightSensors::lightSensorPins); i++) {
//     if (getLight(i) < treshold) {
//       *sensor = i;
//
//       return true;
//     }
//   }
//
//   return false;
// }
