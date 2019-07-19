#include "communicationHandler.h"

bool CommunicationHandler::decode(String message, int *messageType, String *data) {
  char messageCharArr[message.length()];

  message.toCharArray(messageCharArr, message.length());

  int i = 0;

  if (messageCharArr[i] == CommunicationHandler::messageStart) {
    i++;

    if (messageCharArr[i] == CommunicationHandler::lightSensor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_LIGHT_SENSOR;
    }

    else if (messageCharArr[i] == CommunicationHandler::distanceSensor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_DISTANCE_SENSOR;
    }

    else if (messageCharArr[i] == CommunicationHandler::imuSensor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_IMU;
    }

    else if (messageCharArr[i] == CommunicationHandler::motor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_MOTOR;
    }

    else {
      return false;
    }
  }

  else {
    return false;
  }

  return true;
}

String CommunicationHandler::encode(int messageType, String data) {
  String message = "";
  message += CommunicationHandler::messageStart;
  
  if (messageType == TYPE_LIGHT_SENSOR) {
    message += CommunicationHandler::lightSensor;
  }

  else if (messageType == TYPE_DISTANCE_SENSOR) {
    message += CommunicationHandler::distanceSensor;
  }

  else if (messageType == TYPE_IMU) {
    message += CommunicationHandler::imuSensor;
  }

  else if (messageType == TYPE_MOTOR) {
    message += CommunicationHandler::motor;
  }

  else {
    return "";
  }

  message += CommunicationHandler::dataStart;
  message += data;

  message += CommunicationHandler::dataEnd;
  message += CommunicationHandler::messageEnd;

  return message;
}

String CommunicationHandler::readMessage() {
  String message = "";
  if (Serial.read() == CommunicationHandler::messageStart) {
    message += CommunicationHandler::messageStart;
  
    char reading = 'x';

    while (Serial.available() && reading != CommunicationHandler::messageEnd) {
      reading = Serial.read();

      message += reading;

      delay(3);
    }
    
    return message;
  }

  return "";
}

String CommunicationHandler::getDataFromMessage(String message) {
  char messageCharArr[message.length()];

  message.toCharArray(messageCharArr, message.length());

  int i = 0;

  while (messageCharArr[i] != '{') {
    i++;
  }
  i++;
  String data = "";

  while (messageCharArr[i] != '}') {
    data += messageCharArr[i];
    i++;
  }

  return data;
}