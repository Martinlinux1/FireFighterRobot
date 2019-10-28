import time

import serial

import communicationHandler

serialPort = serial.Serial("/dev/ttyUSB0", 115200)
commHandler = communicationHandler.CommunicationHandler(serialPort)

while True:
    time_start = time.time() * 1000
    message = commHandler.read_message()
    for submessage in message:
        print(submessage)
        try:
            message_type, data = commHandler.decode_message(submessage)
        except Exception:
            continue

        if message_type == commHandler.lightSensor:
            line_sensors = data
        elif message_type == commHandler.distanceSensor:
            distance_sensors = data
        elif message_type == commHandler.imuSensor:
            imu_sensor = data
        elif message_type == commHandler.motor or message_type == commHandler.lightSensorsCalibration:
            last_received_message = str(data)
    time_end = time.time() * 1000
    # print(time_end - time_start)
