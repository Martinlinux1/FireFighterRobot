#include "DistanceSensor.h"
DistanceSensor::DistanceSensor(bool useDefaultAddr, int address) {
  DistanceSensor::address = address;

  if (useDefaultAddr) {
    DistanceSensor::sensor.begin();
  }

  else {
    DistanceSensor::sensor.begin(address);
  }
}

int DistanceSensor::read() {
  VL53L0X_RangingMeasurementData_t data;

  DistanceSensor::sensor.rangingTest(&data);

  if (data.RangeStatus != 4) {
    return data.RangeMilliMeter;
  }

  else {
    return -1;
  }
}