import serial
import communicationHandler

serialLink = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

commHandler = communicationHandler.CommunicationHandler(serialLink)

if commHandler.write_motor('A', 'F', 255):
    print('Turning motor A successful')

if commHandler.write_motor('B', 'B', 120):
    print('turning motor B successful')

for i in range(8):
    print(commHandler.get_light_sensor_data(i))

for i in range(5):
    print(commHandler.get_distance_sensor_data(i))

print(commHandler.get_imu_sensor_data())

