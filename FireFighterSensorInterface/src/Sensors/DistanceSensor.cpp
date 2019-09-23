#include "DistanceSensor.h"


DistanceSensor::DistanceSensor(int sensorPin) {
  DistanceSensor::sensorPin = sensorPin;

  pinMode(DistanceSensor::sensorPin, INPUT);
}

int DistanceSensor::read() {
  return digitalRead(DistanceSensor::sensorPin);
}