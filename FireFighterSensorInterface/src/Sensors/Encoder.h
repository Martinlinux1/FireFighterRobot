#include <Arduino.h>
#include <Wire.h>

class Encoder {
  public:
    Encoder(int adress);
    int getDegrees();
    int getRotations();
  private:
    int address;
};