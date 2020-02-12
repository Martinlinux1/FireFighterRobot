#include <Arduino.h>
#include <Wire.h>

class Encoder {
  public:
    Encoder(int adress);
    int getDegrees();
    double getRotations();
    void reset();
  private:
    int address;
};