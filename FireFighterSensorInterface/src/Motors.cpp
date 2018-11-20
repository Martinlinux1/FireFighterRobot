#include "Motors.h"

Motors::Motors(short *motorPins) {
  Motors::motorPins = motorPins;

  for (int i = 0; i < arrLen(Motors::motorPins); i++) {
    ledcSetup(Motors::channels[i], Motors::frequency, Motors::resolution);
    ledcAttachPin(Motors::motorPins[i], Motors::channels[i]);
  }
}

void Motors::motorWrite(char motor, char direction, short speed) {
  if (motor == 'A') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[0], HIGH);
      ledcWrite(Motors::channels[1], LOW);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[0], LOW);
      ledcWrite(Motors::channels[1], HIGH);
    }
  }

  else if (motor == 'B') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[2], HIGH);
      ledcWrite(Motors::channels[3], LOW);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[2], LOW);
      ledcWrite(Motors::channels[3], HIGH);
    }
  }

  else if (motor == 'C') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[4], HIGH);
      ledcWrite(Motors::channels[5], LOW);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[4], LOW);
      ledcWrite(Motors::channels[5], HIGH);
    }
  }

  else if (motor == 'D') {
    if (direction == 'F') {
      ledcWrite(Motors::channels[6], HIGH);
      ledcWrite(Motors::channels[7], LOW);
    }
    else if (direction == 'B') {
      ledcWrite(Motors::channels[6], LOW);
      ledcWrite(Motors::channels[7], HIGH);
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
