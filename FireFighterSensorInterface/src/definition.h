#include <Arduino.h>
#include <Wire.h>
#include "Adafruit_VL53L0X.h"

#define REG_MOTOR_A 0x61  // -> a
#define REG_MOTOR_B 0x62  // -> b
#define REG_MOTOR_C 0x63  // -> c
#define REG_MOTOR_D 0x64  // -> d

#define REG_LIGHT_0 0x65  // -> e
#define REG_LIGHT_1 0x66  // -> f
#define REG_LIGHT_2 0x67  // -> g
#define REG_LIGHT_3 0x68  // -> h
#define REG_LIGHT_4 0x69  // -> i
#define REG_LIGHT_5 0x6A  // -> j
#define REG_LIGHT_6 0x6B  // -> k
#define REG_LIGHT_7 0x6C  // -> l

#define REG_PROX_0 0x6D   // -> m
#define REG_PROX_1 0x6E   // -> n
#define REG_PROX_2 0x6F   // -> o
#define REG_PROX_3 0x70   // -> p
#define REG_PROX_4 0x71   // -> q

#define arrLen(arr) (sizeof(arr) / sizeof(*arr))
