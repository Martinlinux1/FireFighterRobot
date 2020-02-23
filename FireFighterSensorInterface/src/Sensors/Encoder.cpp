#include "Encoder.h"

Encoder::Encoder(int address) {
  Encoder::address = address;
}

int Encoder::getDegrees() {
  return int(Encoder::getRotations() * 360);
}

double Encoder::getRotations() {
  Wire.requestFrom(Encoder::address, 5);
  char receivedData[5];
  
  for (int i = 0; Wire.available(); i++) {
    receivedData[i] = Wire.read();
  }
  int encoderDataRaw = receivedData[0] + (receivedData[1] << 8) + (receivedData[2] << 16) + (receivedData[3] << 24);
  encoderDataRaw = receivedData[5] == 1 ? encoderDataRaw : -encoderDataRaw;
  
  return encoderDataRaw / 8 / 30;
}

void Encoder::reset() {
  Wire.beginTransmission(Encoder::address);
  Wire.write("R");
  Wire.endTransmission();
}
