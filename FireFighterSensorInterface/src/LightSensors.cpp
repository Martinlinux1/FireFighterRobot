#include "LightSensors.h"

LightSensors::LightSensors(short *pins) {
  LightSensors::lightSensorPins = pins;

  for (int i = 0; i < arrLen(pins); i++) {
    pinMode(LightSensors::lightSensorPins[i], INPUT);
  }
}

int LightSensors::getLight(short sensor) {
  return analogRead(LightSensors::lightSensorPins[sensor]);
}

void LightSensors::getLight(int *sensors) {
  for (int i = 0; i < arrLen(LightSensors::lightSensorPins); i++) {
    sensors[i] = getLight(i);
  }
}

bool LightSensors::isLight(int *sensor, int treshold) {
  for (int i = 0; i < arrLen(LightSensors::lightSensorPins); i++) {
    if (getLight(i) < treshold) {
      sensor = i;

      return true;
    }
  }

  return false;
}
