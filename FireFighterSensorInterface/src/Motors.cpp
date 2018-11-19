#include "Motors.h"

Motors::Motors(short *motorPins, int maxSpeed) {
  Motors::motorPins = motorPins;

  Motors::maxSpeed = maxSpeed;

  for (int i = 0; i < arrLen(Motors::motorPins); i++) {
    pinMode(Motors::motorPins[i], OUTPUT);
  }
}

Motors::motorWrite(char motor, char direction, short speed) {
  if (motor == 'A') {
    if (direction == 'F') {
      analogWrite(Motors::motorPins[0], HIGH);
      analogWrite(Motors::motorPins[1], LOW);
    }
    else if (direction == 'B') {
      analogWrite(Motors::motorPins[0], LOW);
      analogWrite(Motors::motorPins[1], HIGH);
    }
  }

  else if (motor == 'B') {
    if (direction == 'F') {
      analogWrite(Motors::motorPins[2], HIGH);
      analogWrite(Motors::motorPins[3], LOW);
    }
    else if (direction == 'B') {
      analogWrite(Motors::motorPins[2], LOW);
      analogWrite(Motors::motorPins[3], HIGH);
    }
  }

  else if (motor == 'C') {
    if (direction == 'F') {
      analogWrite(Motors::motorPins[4], HIGH);
      analogWrite(Motors::motorPins[5], LOW);
    }
    else if (direction == 'B') {
      analogWrite(Motors::motorPins[4], LOW);
      analogWrite(Motors::motorPins[5], HIGH);
    }
  }

  else if (motor == 'D') {
    if (direction == 'F') {
      analogWrite(Motors::motorPins[6], HIGH);
      analogWrite(Motors::motorPins[7], LOW);
    }
    else if (direction == 'B') {
      analogWrite(Motors::motorPins[6], LOW);
      analogWrite(Motors::motorPins[7], HIGH);
    }
  }
}

Motors::writeAB(char direction, short speed) {
  motorWrite('A', direction, speed);
  motorWrite('B', direction, speed);
}

Motors::writeCD(char direction, short speed) {
  motorWrite('C', direction, speed);
  motorWrite('D', direction, speed);
}

Motors::turn(char direction, short speed) {
  if (direction = 'L') {
    motorWrite('A', 'B', speed);
    motorWrite('B', 'B', speed);
    motorWrite('C', 'B', speed);
    motorWrite('D', 'B', speed);
  }
  else if (direction = 'R') {
    motorWrite('A', 'F', speed);
    motorWrite('B', 'F', speed);
    motorWrite('C', 'F', speed);
    motorWrite('D', 'F', speed);
  }
}
