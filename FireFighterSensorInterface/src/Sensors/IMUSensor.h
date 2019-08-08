#include <Arduino.h>


class IMUSensor {
  public:
    IMUSensor(int interruptPin);
    void readIMU();
    float getYawAngle();
    float getPitchAngle();
    float getRollAngle();
    bool init();
    bool initDMP(int XGyroOffset, int YGyroOffset, int ZGyroOffset, int ZAccelOffset);
  private:
};