#include "definition.h"

class Motor {
public:
  Motor(int* ledcChannels);

  void motorWrite(char direction, int speed);
private:
  int *ledcChannels;
};