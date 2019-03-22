#include "definition.h"

class Motors {
public:
  Motors(short *motorPins);

  void motorWrite(char motor, char direction, short speed);

  void forward(String motors, short speed);

  void backward(String motors, short speed);

  void turn(char direction, short speed);
private:
  void ledcAnalogWrite(uint8_t channel, uint32_t value, uint32_t valueMax = 255);
  short *motorPins;
  short channels[8] = {0, 1, 2, 3, 4, 5, 6, 7};
  unsigned int frequency = 1000;
  short resolution = 8;
};
