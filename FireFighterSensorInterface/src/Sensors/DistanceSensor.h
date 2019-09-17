/**
 * VL53L0X distance sensor reader. Can write a different sensor address to use more sensors on i2c bus.
 * Input: The desired sensor addresses, other distance sensors must be turned off, when setuping the sensor.
 *        (by default they have the same address).
 * Output: Reading of the sensor
 * 
 * Creator: Martinlinux
 * Version: 0.0
 */

#include <Arduino.h>


class DistanceSensor {
  public:
    DistanceSensor(int sensorPin);

    bool read();
  private:
    int sensorPin;
};