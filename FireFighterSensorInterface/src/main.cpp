#include <Arduino.h>
#include <Motors/Motor.h>
#include <Sensors/LightSensor.h>
#include <Sensors/DistanceSensor.h>
#include <communicationHandler.h>

int motorPins[8] = {19, 18, 5, 17, 16, 4, 0, 2};
int lightSensorPins[8] = {36, 39, 34, 35, 32, 33, 25, 26};
int motorChannels[4][2] = {
  {0, 1},
  {2, 3},
  {4, 5},
  {6, 7}
};

Motor motors[4] = {
  Motor(motorChannels[0]),
  Motor(motorChannels[1]),
  Motor(motorChannels[2]),
  Motor(motorChannels[3])
};

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

CommunicationHandler commHandler;



void setup() {
  Serial.begin(115200);

  pinMode(2, OUTPUT);

  for (int i = 0; i < 4; i++) {
    for (int j = 0; j < 2; j++) {
      ledcSetup(motorChannels[i][j], 1000, 8);
      ledcAttachPin(motorPins[i + j], motorChannels[i][j]);
    }
  }
}

void loop() {
  if (Serial.available()) {
    digitalWrite(2, HIGH);
    String message = commHandler.readMessage();

    int messageType;
    String data;
    bool isValid = commHandler.decode(message, &messageType, &data);

    if (isValid) {
      String response;
      String responseEncoded;

      if (messageType == TYPE_LIGHT_SENSOR) {
        int sensorIndex = data.toInt();
        response = String(sensorIndex) + ",55";

        responseEncoded = commHandler.encode(TYPE_LIGHT_SENSOR, response);
      }

      else if (messageType == TYPE_DISTANCE_SENSOR) {
        int sensorIndex = data.toInt();

        response = String(sensorIndex) + ",45";
        responseEncoded = commHandler.encode(TYPE_DISTANCE_SENSOR, response);
      }

      else if (messageType == TYPE_IMU) {
        response = "65";
        responseEncoded = commHandler.encode(TYPE_IMU, response);
      }

      else if (messageType == TYPE_MOTOR) {
        String motor = data.substring(0, data.indexOf(","));
        int motorIndex;
        if (motor == "A") {
          motorIndex = 0;
        }

        else if (motor == "B") {
          motorIndex = 1;
        }

        else if (motor == "C") {
          motorIndex = 2;
        }

        else if (motor == "D") {
          motorIndex = 3;
        }

        else {
          return;
        }
        char direction[10];
        data.substring(data.indexOf(",") + 1, data.lastIndexOf(",")).toCharArray(direction, 10);
        int speed = data.substring(data.lastIndexOf(",") + 1, data.indexOf("}")).toInt();

        motors[motorIndex].motorWrite(direction[0], speed);

        response = motor + "," + direction[0] + "," + speed;

        responseEncoded = commHandler.encode(TYPE_MOTOR, response);
      }

      else {
        return; 
      }
      responseEncoded += "\n";
      Serial.print(responseEncoded);
    }
  }
}