/**
 * The sensor interface of fire fighter robot. Reads light, distance(not implemented yet), 
 * angle(not implemented yet) of the robot and controls the motors(4). It communicates with Raspberry Pi 
 * logic unit, that controls the robot.
 * 
 * Creator: Martinlinux
 * Version: 0.0
 */

#include <Arduino.h>
#include <Motors/Motor.h>
#include <Sensors/LightSensor.h>
#include <Sensors/DistanceSensor.h>
#include <Sensors/IMUSensor.h>
#include <communicationHandler.h>



int motorPins[8] = {19, 18, 17, 5, 2, 0, 4, 16};
int lightSensorPins[8] = {36, 39, 34, 35, 32, 33, 25, 26};
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

// Creates light sensor class instance.
LightSensor lightSensors[8] = {
  LightSensor(lightSensorPins[0]),
  LightSensor(lightSensorPins[1]),
  LightSensor(lightSensorPins[2]),
  LightSensor(lightSensorPins[3]),
  LightSensor(lightSensorPins[4]),
  LightSensor(lightSensorPins[5]),
  LightSensor(lightSensorPins[6]),
  LightSensor(lightSensorPins[7])
};

IMUSensor mpu(imuInterruptPin);

// Creates communicationHandler class instance.
CommunicationHandler commHandler;

TaskHandle_t readIMUSensor;
void readMPU(void * param) {
  for (;;) {
    mpu.readIMU();
  }
}

// Setup function.
void setup() {
  // Serial link setup.
  Serial.begin(115200);

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

  mpu.init();
  mpu.initDMP(220, 76, -20, 2008);
  xTaskCreatePinnedToCore(
                    readMPU,        /* Task function. */
                    "Task1",        /* name of task. */
                    10000,          /* Stack size of task */
                    NULL,           /* parameter of the task */
                    1,              /* priority of the task */
                    &readIMUSensor, /* Task handle to keep track of created task */
                    0);             /* pin task to core 0 */
}

// Loop function.
void loop() {
  digitalWrite(0, LOW);
  digitalWrite(2, LOW);
  // If request was sent from RPi.
  noInterrupts();
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

      // If request's type is light sensor.
      if (messageType == TYPE_LIGHT_SENSOR) {
        int sensorIndex = data.toInt();
        // Read the light sensor.
        int lightSensorReading = lightSensors[sensorIndex].read();

        // Form the response
        response = String(sensorIndex) + "," + String(lightSensorReading);
        
        // Encode the response.
        responseEncoded = commHandler.encode(TYPE_LIGHT_SENSOR, response);
      }

      // If the request's type is distance sensor.
      else if (messageType == TYPE_DISTANCE_SENSOR) {
        int sensorIndex = data.toInt();
        int reading = lightSensors[sensorIndex].read();
        
        // Form the response.
        response = String(sensorIndex) + ",45";

        // Encode the response.
        responseEncoded = commHandler.encode(TYPE_DISTANCE_SENSOR, response);
      }

      // If the request's type is IMU sensor.
      else if (messageType == TYPE_IMU) {
        // Form the response.
        response = String(mpu.getYawAngle());

        // Encode the response.
        responseEncoded = commHandler.encode(TYPE_IMU, response);
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
        responseEncoded = commHandler.encode(TYPE_MOTOR, response);
      }

      // Invalid request.
      else {
        return; 
      }

      // Send the response.
      responseEncoded += "\n";
      Serial.print(responseEncoded);
    }
  }
  interrupts();
}