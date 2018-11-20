#include "definition.h"

class LightSensors {
public:
  LightSensors(short *pins);

  int getLight(short sensor);

  void getLight(int *sensors);

  bool isLight(int *sensor, int treshold);
private:
  short *lightSensorPins;
};
