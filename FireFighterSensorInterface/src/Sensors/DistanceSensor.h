#include "definition.h"
#include <Adafruit_Sensor.h>
#include <Adafruit_VL53L0X.h>

class DistanceSensor {
  public:
    DistanceSensor(bool useDefaultAddr, int address = 0x29);
    int read();
  private:
    Adafruit_VL53L0X sensor = Adafruit_VL53L0X();
    int address;
};