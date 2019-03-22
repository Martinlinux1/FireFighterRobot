#include "ProximitySensors.h"

ProximitySensors::ProximitySensors(short *sensorsPins) {
  for (size_t i = 0; i < arrLen(ProximitySensors::sensorAddress); i++) {
    
  }

  for (size_t i = 0; i < arrLen(ProximitySensors::sensorAddress); i++) {
    ProximitySensors::proxSensors[i].begin(ProximitySensors::sensorAddress[i]);
  }
}

float ProximitySensors::getProximity(short sensor) {
  VL53L0X_RangingMeasurementData_t measure;

  ProximitySensors::proxSensors[sensor].rangingTest(&measure, false);

  if (measure.RangeStatus != 4) {
    return measure.RangeMilliMeter;
  }

  else {
    return -1;
  }
}

void ProximitySensors::getProximity(float *sensors) {
  for (size_t i = 0; i < arrLen(ProximitySensors::sensorAddress); i++) {
    sensors[i] = getProximity(i);
  }
}

bool ProximitySensors::isWall(float treshold, short *sensor) {
  for (size_t i = 0; i < arrLen(ProximitySensors::sensorAddress); i++) {
    if (getProximity(i)) {
      *sensor = i;

      return true;
    }
  }

  *sensor = -1;

  return false;
}
