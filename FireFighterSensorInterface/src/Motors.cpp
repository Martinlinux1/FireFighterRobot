#include "Motors.h"

Motors::Motors(short *motorPins) {
  Motors::motorPins = motorPins;

  for (int i = 0; i < arrLen(Motors::motorPins); i++) {
    ledcSetup(Motors::channels[i], Motors::frequency, LEDC_TIMER_13_BIT);
    ledcAttachPin(Motors::motorPins[i], Motors::channels[i]);
  }
}

void Motors::motorWrite(char motor, char direction, short speed) {
  if (motor == 'A') {
    if (direction == 'F') {
      Motors::ledcAnalogWrite(Motors::channels[0], speed);
      Motors::ledcAnalogWrite(Motors::channels[0], 0);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[0], 0);
      ledcWrite(Motors::channels[1], speed);
    }
  }

  else if (motor == 'B') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[2], speed);
      ledcWrite(Motors::channels[3], 0);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[2], 0);
      ledcWrite(Motors::channels[3], speed);
    }
  }

  else if (motor == 'C') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[4], speed);
      ledcWrite(Motors::channels[5], 0);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[4], 0);
      ledcWrite(Motors::channels[5], speed);
    }
  }

  else if (motor == 'D') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[6], speed);
      ledcWrite(Motors::channels[7], 0);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[6], 0);
      ledcWrite(Motors::channels[7], speed);
    }
  }
}

void Motors::forward(String motors, short speed) {
  char *motor1;
  char *motor2;

  motors.substring(0, 1).toCharArray(motor1, 1);
  motors.substring(1).toCharArray(motor2, 1);

  motorWrite(motor1[0], 'F', speed);
  motorWrite(motor2[0], 'F', speed);
}

void Motors::backward(String motors, short speed) {
  char *motor1;
  char *motor2;

  motors.substring(0, 1).toCharArray(motor1, 1);
  motors.substring(1).toCharArray(motor2, 1);

  motorWrite(motor1[0], 'B', speed);
  motorWrite(motor2[0], 'B', speed);
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

void Motors::ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax = 255) {
  // calculate duty, 8191 from 2 ^ 13 - 1
  uint32_t duty = (8191 / valueMax) * min(value, valueMax);

  // write duty to LEDC
  ledcWrite(channel, duty);
}
