/**
 * Simple digital IR sensor reader.
 * Input: Sensor pin.
 * Output: Reading of the sensor
 * 
 * Creator: Martinlinux
 * Version: 0.1
 */

#include <Arduino.h>


class DistanceSensor {
  public:
    DistanceSensor(int sensorPin);

    bool read();
  private:
    int sensorPin;
};