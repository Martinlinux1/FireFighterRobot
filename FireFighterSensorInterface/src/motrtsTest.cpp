#include "definition.h"
#include "Motors.h"

short motorPins[8] = {19, 18, 5, 17, 16, 4, 0, 2};

Motors motors(motorPins);

void setup() {

}

void loop() {
  motors.forward("AB", 255);
}
