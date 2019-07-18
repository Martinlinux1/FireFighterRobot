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

    if (messageCharArr[i] == CommunicationHandler::distanceSensor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_DISTANCE_SENSOR;
    }

    if (messageCharArr[i] == CommunicationHandler::imuSensor) {
      i++;
      *data = CommunicationHandler::getDataFromMessage(message);
      *messageType = TYPE_IMU;
    }

    if (messageCharArr[i] == CommunicationHandler::motor) {
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