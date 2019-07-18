#include "definition.h"

#define TYPE_LIGHT_SENSOR 0
#define TYPE_DISTANCE_SENSOR 1
#define TYPE_MOTOR 2
#define TYPE_IMU 3

class CommunicationHandler {
  public:
    String readMessage();

    bool decode(String message, int *messageType, String *data);

    String encode(int messageType, String data);
  private:
    String getDataFromMessage(String message);

    const char lightSensor = 'L';
    const char distanceSensor = 'D';
    const char imuSensor = 'I';
    const char motor = 'M';
    const char messageStart = '<';
    const char messageEnd = '>';
    const char dataStart = '{';
    const char dataEnd = '}';
};