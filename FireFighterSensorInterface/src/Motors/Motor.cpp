#include "Motor.h"

Motor::Motor(int *ledcChannels) {
  Motor::ledcChannels = ledcChannels;
}

void Motor::motorWrite(char direction, int speed) {
  if (direction == 'F') {
    ledcWrite(Motor::ledcChannels[0], speed);
    ledcWrite(Motor::ledcChannels[1], 0);
  }
  else if (direction == 'B') {
    ledcWrite(Motor::ledcChannels[0], 0);
    ledcWrite(Motor::ledcChannels[1], speed);
  }
}