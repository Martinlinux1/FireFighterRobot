#include "definition.h"

class Motors {
public:
  Motors(short *motorPins, int maxSpeed);

  void motorWrite(char motor, char direction, short speed);

  void writeAB(char direction, short speed);
  void writeCD(char direction, short speed);

  void turn(char direction, short speed);
private:
  short *motorPins;
  int maxSpeed;
}
