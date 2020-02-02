/**
 * The sensor interface of fire fighter robot. Reads light, distance, 
 * angle of the robot and controls the motors(4). It communicates with Raspberry Pi 
 * logic unit, that controls the robot.
 * 
 * Creator: Martinlinux
 * Version: 1.0
 */

#include <Arduino.h>
#include <Wire.h>
#include <qtr-sensors-arduino-master/QTRSensors.h>
#include <Motors/Motor.h>
#include <Sensors/LightSensor.h>
#include <Sensors/DistanceSensor.h>
#include <Sensors/IMUSensor.h>
#include <Sensors/Encoder.h>
#include <communicationHandler.h>



int motorPins[8] = {19, 18, 17, 5, 2, 0, 4, 16};
uint8_t lightSensorPins[8] = {36, 39, 34, 35, 32, 33, 25, 26};
int distanceSensorPins[5] = {27, 14, 12, 13, 23};
int motorChannels[4][2] = {
  {0, 1},
  {2, 3},
  {4, 5},
  {6, 7}
};

int imuInterruptPin = 15;

// Creates motor class instance.
Motor motors[4] = {
  Motor(motorChannels[0]),
  Motor(motorChannels[1]),
  Motor(motorChannels[2]),
  Motor(motorChannels[3])
};

QTRSensors lineSensors;

DistanceSensor distanceSensors[5] = {
  DistanceSensor(distanceSensorPins[0]),
  DistanceSensor(distanceSensorPins[1]),
  DistanceSensor(distanceSensorPins[2]),
  DistanceSensor(distanceSensorPins[3]),
  DistanceSensor(distanceSensorPins[4])
};

Encoder encoders[4] = {
  Encoder(0x10),
  Encoder(0x11),
  Encoder(0x12),
  Encoder(0x13)
};

IMUSensor mpu(imuInterruptPin);

// Creates communicationHandler class instance.
CommunicationHandler commHandler;

TaskHandle_t readIMUSensor;

void readMPU(void * param) {
  for (;;) {
    mpu.readIMU();
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

// Setup function.
void setup() {
  // Serial link setup.
  Serial.begin(115200);
  Wire.begin();

  // Motors pins setup.
  int k = 0;
  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 2; j++) {
      pinMode(motorPins[k], OUTPUT);
      ledcSetup(motorChannels[i][j], 1000, 8);
      ledcAttachPin(motorPins[k], motorChannels[i][j]);
      k++;
    }
  }

  lineSensors.setTypeAnalog();
  lineSensors.setSensorPins(lightSensorPins, 8);


  digitalWrite(0, LOW);
  digitalWrite(2, LOW);

  mpu.init();
  mpu.initDMP(63, 40, -20, -957, 2311, 1710);  // These values are device specific, to find them, use this program: https://wired.chillibasket.com/2015/01/calibrating-mpu6050/

  xTaskCreatePinnedToCore(
    readMPU,
    "IMU reading task",
    100000,
    NULL,
    0,
    &readIMUSensor,
    0);

  Serial.println(xPortGetCoreID());
}

// Loop function.
void loop() {
  if (Serial.available()) { 
    // Read the request.
    String message = commHandler.readMessage();

    int messageType;
    String data;
    // Decode the request.
    
    bool isValid = commHandler.decode(message, &messageType, &data);
    // If the request is valid.
    if (isValid) {
      String response;
      String responseEncoded;

      if (messageType == TYPE_DATA) {
        uint16_t sensorValues[8];
        lineSensors.read(sensorValues);

        String lightSensorsData = "";
        String distanceSensorsData = "";
        String IMUSensorData = "";

        for (int i = 0; i < 8; i++) {
          lightSensorsData += String(sensorValues[i]) + ",";
          if (i < 5) {
            distanceSensorsData += String(distanceSensors[i].read()) + ",";
          }
        }

        IMUSensorData = String(mpu.getYawAngle());

        lightSensorsData = lightSensorsData.substring(0, lightSensorsData.lastIndexOf(','));
        String lightSensorsDataEncoded = commHandler.encode(TYPE_LIGHT_SENSOR, lightSensorsData);

        distanceSensorsData = distanceSensorsData.substring(0, distanceSensorsData.lastIndexOf(','));
        String distanceSensorsDataEncoded = commHandler.encode(TYPE_DISTANCE_SENSOR, distanceSensorsData);

        String IMUSensorDataEncoded = commHandler.encode(TYPE_IMU, IMUSensorData);

        responseEncoded = '~' + lightSensorsDataEncoded + '\t' + distanceSensorsDataEncoded + '\t' + IMUSensorDataEncoded;
      }

      else if (messageType == TYPE_ENCODER) {
        String encodersData;

        for (int i = 0; i < 4; i++) {
          encodersData += String(encoders[i].getRotations()) + ",";
        }

        responseEncoded = "~" + commHandler.encode(TYPE_ENCODER, encodersData);
      }

      else if (messageType == TYPE_MOTOR) {
        // Get the motor to be turned on.
        String motor = data.substring(0, data.indexOf(","));
        int motorIndex;

        // Motor A -> motor 0.
        if (motor == "A") {
          motorIndex = 0;
        }

        // Motor B -> motor 1.
        else if (motor == "B") {
          motorIndex = 1;
        }

        // Motor C -> motor 2.
        else if (motor == "C") {
          motorIndex = 2;
        }

        // Motor D -> motor 3.
        else if (motor == "D") {
          motorIndex = 3;
        }

        // Invalid request.
        else {
          return;
        }

        // Get the direction.
        char direction[10];
        data.substring(data.indexOf(",") + 1, data.lastIndexOf(",")).toCharArray(direction, 10);
        int speed = data.substring(data.lastIndexOf(",") + 1, data.indexOf("}")).toInt();
        
        // Write the motor.
        motors[motorIndex].motorWrite(direction[0], speed);

        // Form the response.
        response = motor + "," + direction[0] + "," + speed;
        
        // Encode the response.
        responseEncoded = "~" + commHandler.encode(TYPE_MOTOR, response);
      }

      else if (messageType == TYPE_MOTORS_BRAKE) {
        motors[0].brake();
        motors[1].brake();
        motors[2].brake();
        motors[3].brake();

        responseEncoded = '~' + message;
      }

      // Invalid request.
      else {
        return; 
      }

      // Send the response.
      responseEncoded += "\n";
      Serial.print(responseEncoded);
      long timeEnd = micros();
    }
  }
}