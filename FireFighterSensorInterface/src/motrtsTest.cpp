#include "definition.h"
#include "Motors.h"

short motorPins[8] = {19, 18, 5, 17, 16, 4, 0, 2};

Motors motors(motorPins);

void setup() {
  Serial.begin(9600);
  pinMode(5, OUTPUT);
  digitalWrite(5, LOW);
  pinMode(0, OUTPUT);
  digitalWrite(0, LOW);
  pinMode(15, OUTPUT);
  digitalWrite(15, LOW);
}

void loop() {
  motors.forward("AB", 255);
  motors.motorWrite('B', 'F', 255);
  motors.motorWrite('C', 'F', 127);
  motors.motorWrite('D', 'B', 127);
}
