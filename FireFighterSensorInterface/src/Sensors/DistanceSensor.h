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
#include <Adafruit_Sensor.h>
#include <Adafruit_VL53L0X.h>


class DistanceSensor {
  public:
    ///<summary> VL53L0X distance sensor reader.
    ///<param name="useDefaultAddr"> Use default I2C address of the sensor.
    ///<param name="address"> Optional, I2C address to set the sensor.
    DistanceSensor(bool useDefaultAddr, int address = 0x29);

    ///<summary> Read the sensor's data.
    int read();
  private:
    Adafruit_VL53L0X sensor = Adafruit_VL53L0X();
    int address;
};