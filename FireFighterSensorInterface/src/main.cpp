#include <Arduino.h>
#include <Motors/Motor.h>
#include <Sensors/LightSensor.h>
#include <Sensors/DistanceSensor.h>

int motorPins[8] = {19, 18, 5, 17, 16, 4, 0, 2};
int lightSensorPins[8] = {36, 39, 34, 35, 32, 33, 25, 26};
int motorChannels[4][2] = {
  {0, 1},
  {2, 3},
  {4, 5},
  {6, 7}
};

Motor motors[4] = {
  Motor(motorChannels[0]),
  Motor(motorChannels[1]),
  Motor(motorChannels[2]),
  Motor(motorChannels[3])
};

LightSensor lightSensors[8] = {
  LightSensor(lightSensorPins[0]),
  LightSensor(lightSensorPins[1]),
  LightSensor(lightSensorPins[2]),
  LightSensor(lightSensorPins[3]),
  LightSensor(lightSensorPins[4]),
  LightSensor(lightSensorPins[5]),
  LightSensor(lightSensorPins[6]),
  LightSensor(lightSensorPins[7])
};


void setup() {
  
}

void loop() {
  motors[0].motorWrite('F', 255);
  motors[1].motorWrite('F', 255);
}