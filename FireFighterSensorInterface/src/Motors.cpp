#include "Motors.h"

Motors::Motors(short *motorPins) {
  Motors::motorPins = motorPins;

  for (int i = 0; i < 8; i++) {
    pinMode(Motors::motorPins[i], OUTPUT);
    ledcSetup(Motors::channels[i], Motors::frequency, 13);
    ledcAttachPin(Motors::motorPins[i], Motors::channels[i]);
  }

  digitalWrite(0, LOW);
  digitalWrite(15, LOW);
  digitalWrite(5, LOW);
}

void Motors::motorWrite(char motor, char direction, short speed) {
  if (motor == 'A') {
    if (direction == 'F') {
      Motors::ledcAnalogWrite(Motors::channels[0], speed);
      Motors::ledcAnalogWrite(Motors::channels[1], 0);
    }
    else if (direction == 'B') {
      Motors::ledcAnalogWrite(Motors::channels[0], 0);
      Motors::ledcAnalogWrite(Motors::channels[1], speed);
    }
  }

  else if (motor == 'B') {
    if (direction == 'F') {
      Motors::ledcAnalogWrite(Motors::channels[2], speed);
      Motors::ledcAnalogWrite(Motors::channels[3], 0);
    }
    else if (direction == 'B') {
      Motors::ledcAnalogWrite(Motors::channels[2], 0);
      Motors::ledcAnalogWrite(Motors::channels[3], speed);
    }
  }

  else if (motor == 'C') {
    if (direction == 'F') {
      Motors::ledcAnalogWrite(Motors::channels[4], speed);
      Motors::ledcAnalogWrite(Motors::channels[5], 0);
    }
    else if (direction == 'B') {
      Motors::ledcAnalogWrite(Motors::channels[4], 0);
      Motors::ledcAnalogWrite(Motors::channels[5], speed);
    }
  }

  else if (motor == 'D') {
    if (direction == 'F') {
      Motors::ledcAnalogWrite(Motors::channels[6], speed);
      Motors::ledcAnalogWrite(Motors::channels[7], 0);
    }
    else if (direction == 'B') {
      Motors::ledcAnalogWrite(Motors::channels[6], 0);
      Motors::ledcAnalogWrite(Motors::channels[7], speed);
    }
  }
}

void Motors::forward(String motors, short speed) {
  char motorsC[2];

  motors.toCharArray(motorsC, 2);

  motorWrite(motorsC[0], 'F', speed);
  motorWrite(motorsC[1], 'F', speed);
}

void Motors::backward(String motors, short speed) {
  char motorsC[5];

  Serial.println(motors);

  motors.toCharArray(motorsC, 5);

  Serial.println(motorsC[0]);
  Serial.println(motorsC[1]);

  motorWrite(motorsC[0], 'B', speed);
  motorWrite(motorsC[1], 'B', speed);
}

void Motors::turn(char direction, short speed) {
  if (direction == 'L') {
    motorWrite('A', 'B', speed);
    motorWrite('B', 'F', speed);
    motorWrite('C', 'B', speed);
    motorWrite('D', 'F', speed);
  }
  else if (direction == 'R') {
    motorWrite('A', 'F', speed);
    motorWrite('B', 'B', speed);
    motorWrite('C', 'F', speed);
    motorWrite('D', 'B', speed);
  }
}

void Motors::ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax) {
  // calculate duty, 8191 from 2 ^ 13 - 1
  uint32_t duty = (8191 / valueMax) * min(value, valueMax);

  // write duty to LEDC
  ledcWrite(channel, duty);
}
