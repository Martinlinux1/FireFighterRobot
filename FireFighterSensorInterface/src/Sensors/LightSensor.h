#include "definition.h"

class LightSensor {
  public:
    LightSensor(int lightSensorPin, int resolution = 12);
    int read();
  private:
    int lightSensorPin;
    int resolution;
};
