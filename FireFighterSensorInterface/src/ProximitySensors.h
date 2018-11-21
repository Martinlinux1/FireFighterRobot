#include "definition.h"
#include "Adafruit_VL53L0X.h"

class ProximitySensors {
public:
  ProximitySensors();

  float getProximity(short sensor);

  void getProximity(float *sensors);

  bool isWall(float treshold, short *sensor);
private:
  Adafruit_VL53L0X proxSensors[5];

  short sensorAddress[5] = {0x25, 0x26, 0x27, 0x28, 0x29};
};
