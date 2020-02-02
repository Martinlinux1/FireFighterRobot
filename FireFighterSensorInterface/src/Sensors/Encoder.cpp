#include "Encoder.h"

Encoder::Encoder(int address) {
  Encoder::address = address;
}

int Encoder::getDegrees() {
  Wire.requestFrom(Encoder::address, 10);
  String encoderData = "";
  
  while (Wire.available()) {
    encoderData += Wire.read();
  }

  return encoderData.toInt();
}

double Encoder::getRotations() {
  return Encoder::getDegrees() / 360;
}