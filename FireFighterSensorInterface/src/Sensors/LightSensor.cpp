#include "LightSensor.h"

LightSensor::LightSensor(int lightSensorPin, int resolution) {
  LightSensor::lightSensorPin = lightSensorPin;
  LightSensor::resolution = resolution;

  analogReadResolution(resolution);
}

int LightSensor::read() {
  int reading = analogRead(LightSensor::lightSensorPin);

  return reading;
}