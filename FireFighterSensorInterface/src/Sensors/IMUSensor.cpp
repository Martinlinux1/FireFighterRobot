#include "IMUSensor.h"
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include <Wire.h>

bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer
Quaternion q;           // [w, x, y, z]         quaternion container
VectorFloat gravity;    // [x, y, z]            gravity vector
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

MPU6050 imu;


volatile bool mpuInterrupt = false;
void IRAM_ATTR dmpDataReady() {
  mpuInterrupt = true;
}

IMUSensor::IMUSensor(int interruptPin) {
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), dmpDataReady, RISING);
  Wire.begin();
  Wire.setClock(400000);
}

bool IMUSensor::init() {
  imu.initialize();
  return imu.testConnection();
}

bool IMUSensor::initDMP(int XGyroOffset, int YGyroOffset, int ZGyroOffset, int XAccelOffset, int YAccelOffset, int ZAccelOffset) {
  devStatus = imu.dmpInitialize();

  imu.setXGyroOffset(XGyroOffset);
  imu.setYGyroOffset(YGyroOffset);
  imu.setZGyroOffset(ZGyroOffset);
  imu.setXAccelOffset(XAccelOffset);
  imu.setYAccelOffset(YAccelOffset);
  imu.setZAccelOffset(ZAccelOffset);

  if (devStatus == 0) {
    imu.CalibrateAccel(6);
    imu.CalibrateGyro(6);
    
    imu.setDMPEnabled(true);
    mpuIntStatus = imu.getIntStatus();

    packetSize = imu.dmpGetFIFOPacketSize();
  }

  else {
    return false;
  }

  return true;
}

void IMUSensor::readIMU() {
  while (!mpuInterrupt && fifoCount < packetSize) {
    if (mpuInterrupt && fifoCount < packetSize) {
      fifoCount = imu.getFIFOCount();
    }  
  }

  mpuInterrupt = false;
  mpuIntStatus = imu.getIntStatus();

  fifoCount = imu.getFIFOCount();

  if(fifoCount < packetSize){}
  else if ((mpuIntStatus & _BV(MPU6050_INTERRUPT_FIFO_OFLOW_BIT)) || fifoCount >= 1024) {
      imu.resetFIFO();

  } else if (mpuIntStatus & _BV(MPU6050_INTERRUPT_DMP_INT_BIT)) {
  	while(fifoCount >= packetSize){ 
  		imu.getFIFOBytes(fifoBuffer, packetSize);
  		fifoCount -= packetSize;
  	}
  
    imu.dmpGetQuaternion(&q, fifoBuffer);
    imu.dmpGetGravity(&gravity, &q);
    imu.dmpGetYawPitchRoll(ypr, &q, &gravity);
  }
}

float IMUSensor::getYawAngle() {
  return ypr[0] * 180 / PI;
}

float IMUSensor::getPitchAngle() {
  return ypr[1] * 180 / PI;
}

float IMUSensor::getRollAngle() {
  return ypr[2] * 180 / PI;
}