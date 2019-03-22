#include "definition.h"
#include "Adafruit_VL53L0X.h"

class ProximitySensors {
public:
  ProximitySensors(short *sensorsPins);

  float getProximity(short sensor);

  void getProximity(float *sensors);

  bool isWall(float treshold, short *sensor);
private:
  Adafruit_VL53L0X proxSensors[5];

  short sensorAddress[5] = {0x29, 0x2A, 0x2B, 0x2C, 0x2D};
};
