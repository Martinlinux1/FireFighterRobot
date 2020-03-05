#include "Encoder.h"

Encoder::Encoder(int address) {
  Encoder::address = address;
}

int Encoder::getDegrees() {
  return int(Encoder::getRotations() * 360);
}

double Encoder::getRotations() {
  Wire.requestFrom(Encoder::address, 4);

  union longToBytes {
    char buffer[4];
    long value;
  } converter;

  for (int i = 0; Wire.available(); i++) {
    converter.buffer[i] = Wire.read();
  }

  long encoderDataRaw = converter.value;

  return encoderDataRaw / 8 / 30;
}

void Encoder::reset() {
  Wire.beginTransmission(Encoder::address);
  Wire.write("R");
  Wire.endTransmission();
}
