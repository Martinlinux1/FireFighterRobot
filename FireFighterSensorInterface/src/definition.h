#include <Arduino.h>
#include "Adafruit_VL53L0X.h"

#define RASPBERRY_PI_I2C_ADDRESS 0x44

#define REG_MOTOR_A 0x01
#define REG_MOTOR_B 0x02
#define REG_MOTOR_C 0x03
#define REG_MOTOR_D 0x04

#define REG_LIGHT_0 0x05
#define REG_LIGHT_1 0x06
#define REG_LIGHT_2 0x07
#define REG_LIGHT_3 0x08
#define REG_LIGHT_4 0x09
#define REG_LIGHT_5 0x10
#define REG_LIGHT_6 0x11
#define REG_LIGHT_7 0x12

#define REG_PROX_0 0x13
#define REG_PROX_1 0x14
#define REG_PROX_2 0x15
#define REG_PROX_3 0x16
#define REG_PROX_4 0x17

#define arrLen(arr) (sizeof(arr) / sizeof(*arr))
