#include <Arduino.h>
#include <Wire.h>

class Encoder {
  public:
    Encoder(int adress, int countsPerRevolution, int gearbox);
    int getDegrees();
    double getRotations();
    void reset();
  private:
    int address;
    int countsPerRevolution;
    int gearbox;
};