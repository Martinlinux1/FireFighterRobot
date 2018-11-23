#include "definition.h"
#include "Motors.h"
#include "LightSensors.h"

short motorPins[8] = {19, 18, 5, 15, 8, 9, 10, 11};
short lightSensorsPins[8] = {32, 33, 25, 26, 27, 14, 12, 13};


Motors motors(motorPins);
LightSensors lightSensors(lightSensorsPins);


void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    int reg = Serial.read();

    if (Serial.available()) {
      int speed = Serial.read();

      if (reg == REG_MOTOR_A) {
        // char direction = speed < 0 ? 'B' : 'F';
        //
        // speed = speed  < 0 ? speed + speed * 2 : speed;
        //
        // speed *= 2;
        // motors.motorWrite('A', direction, speed);

        Serial.print("Motor A with speed: ");
        Serial.println(speed);
      }

      else if (reg == REG_MOTOR_B) {
        // char direction = speed < 0 ? 'B' : 'F';
        //
        // speed = speed  < 0 ? speed + speed * 2 : speed;
        //
        // speed *= 2;
        // motors.motorWrite('B', direction, speed);

        Serial.print("Motor B with speed: ");
        Serial.println(speed);
      }

      else if (reg == REG_MOTOR_C) {
        // char direction = speed < 0 ? 'B' : 'F';
        //
        // speed = speed  < 0 ? speed + speed * 2 : speed;
        //
        // speed *= 2;
        // motors.motorWrite('C', direction, speed);

        Serial.print("Motor C with speed: ");
        Serial.println(speed);
      }

      else if (reg == REG_MOTOR_D) {
        // char direction = speed < 0 ? 'B' : 'F';
        //
        // speed = speed  < 0 ? speed + speed * 2 : speed;
        //
        // speed *= 2;
        // motors.motorWrite('D', direction, speed);

        Serial.print("Motor D with speed: ");
        Serial.println(speed);
      }
    }

    else if (reg == REG_LIGHT_0) {
      // Serial.write(lightSensors.getLight(0));
      Serial.println("Light sensor 0");
    }

    else if (reg == REG_LIGHT_1) {
      // Serial.write(lightSensors.getLight(1));
      Serial.println("Light sensor 1");
    }

    else if (reg == REG_LIGHT_2) {
      // Serial.write(lightSensors.getLight(2));
      Serial.println("Light sensor 2");
    }

    else if (reg == REG_LIGHT_3) {
      // Serial.write(lightSensors.getLight(3));
      Serial.println("Light sensor 3");
    }

    else if (reg == REG_LIGHT_4) {
      // Serial.write(lightSensors.getLight(4));
      Serial.println("Light sensor 4");
    }

    else if (reg == REG_LIGHT_5) {
      // Serial.write(lightSensors.getLight(5));
      Serial.println("Light sensor 5");
    }

    else if (reg == REG_LIGHT_6) {
      // Serial.write(lightSensors.getLight(6));
      Serial.println("Light sensor 6");
    }

    else if (reg == REG_LIGHT_7) {
      // Serial.write(lightSensors.getLight(7));
      Serial.println("Light sensor 7");
    }

    else if (reg == REG_PROX_0) {
      Serial.println("Proximity sensor 0");
    }

    else if (reg == REG_PROX_1) {
      Serial.println("Proximity sensor 1");
    }

    else if (reg == REG_PROX_2) {
      Serial.println("Proximity sensor 2");
    }

    else if (reg == REG_PROX_3) {
      Serial.println("Proximity sensor 3");
    }

    else if (reg == REG_PROX_4) {
      Serial.println("Proximity sensor 4");
    }
  }
}
