import threading
from time import sleep

import serial

import communicationHandler
import motorController
from MathUtils import MathUtils
from cameraReader import CameraReader


# from gpiozero import DigitalOutputDevice
# from gpiozero import Servo


# Camera reader
class CameraFetcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        while self.is_alive():
            ir = [0]
            # ir = cam.read_camera()

            # if 0 in ir:
            #     print("camera reading failure")
            # else:
            #     print("camera reading successful")
            camera_data_read_event.set()


class SerialReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        global line_sensors
        global distance_sensors
        global imu_sensor
        global last_received_message

        while True:
            message = commHandler.read_message()
            for submessage in message:
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
                last_received_message = str(data)


class LineSensorsReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        global sensors_on_line

        while True:
            line_detected_sensors = []

            if not line_sensors:
                continue

            for i in range(8):
                if line_sensors[i] > lightSensorsBlack:
                    line_detected_sensors.append(i)

            sensors_on_line = line_detected_sensors


class DistanceSensorsReader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        global obstacles
        while True:
            sensors_detected = []

            if not distance_sensors:
                continue

            for i in range(5):
                if not distance_sensors[i]:
                    sensors_detected.append(i)

            obstacles = sensors_detected


def fire_after_obstacle(direction: str):
    global obstacles
    if direction == 'right':
        while 2 in obstacles:
            motors.forward(baseSpeed)
        sleep(0.2)
        motors.brake()
        motors.turn(90, baseSpeed)
        motors.forward(baseSpeed)
        sleep(0.3)

    if direction == 'left':
        while 2 in obstacles:
            motors.forward(baseSpeed)
        sleep(0.2)
        motors.brake()
        motors.turn(-90, baseSpeed)
        motors.forward(baseSpeed)
        sleep(0.3)


camera_data_read_event = threading.Event()

turned = False
fanPin = 4

# fan = DigitalOutputDevice(fanPin, False)
# servo = Servo(14)
# onLineLED = DigitalOutputDevice(15)

# thermal_camera = pyusb2fir.USB2FIR(refreshRate=5)
serialPort = serial.Serial("/dev/ttyUSB0", 115200)

t1 = CameraFetcher()
t1.daemon = True

t2 = SerialReader()
t2.daemon = True

t3 = LineSensorsReader()
t3.daemon = True

t4 = DistanceSensorsReader()
t4.daemon = True

# cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.

baseSpeed = 150

lightSensorsBlack = 300

line_sensors = []
sensors_on_line = []
distance_sensors = []
obstacles = []
imu_sensor = -999
last_received_message = ''

t1.start()
t2.start()
t3.start()
t4.start()

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)
print('calibrating light sensors...')
commHandler.calibrate_light_sensors()

while not (commHandler.lightSensorsCalibration in last_received_message):
    print(sensors_on_line, obstacles, imu_sensor)
    pass

print('DONE.')

while True:
    try:
        camera_data_read_event.wait()
        fire_coordinates = cam.is_fire(40)
        camera_data_read_event.clear()

        if fire_coordinates[0]:
            print("Fire on: ", fire_coordinates)

            all_fire_angles = cam.coordinates_to_angle(fire_coordinates[1])

            print("Robot needs to turn: ", all_fire_angles)

            max_val = [0, 0, 0]
            for i in fire_coordinates[1]:
                if i[2] > max_val[2]:
                    max_val = i

            print("Fire closest to robot: ", max_val)
            max_fire_angle = CameraReader.coordinates_to_angle(fire_coordinates)

            print("Robot turning: ", max_fire_angle)

            if max_fire_angle[0] > 30 or max_fire_angle[0] < -30:
                if max_fire_angle[0] > 0:
                    motors.turn_manual('L', baseSpeed)
                else:
                    motors.turn_manual('R', baseSpeed)
            else:
                pass
                motors.slide(max_fire_angle[0] * -1, baseSpeed)

            if max_fire_angle[0] < 15 and 0 in sensors_on_line:
                print("Extinguishing")
                motors.brake()
                servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

                # servo.value = servo_angle
                # fan.on()

        elif sensors_on_line:
            # onLineLED.on()
            print('line')

            if 6 in sensors_on_line and 5 in sensors_on_line and 4 in sensors_on_line:  # Left downer corner.
                motors.turn(45, baseSpeed)
            elif 2 in sensors_on_line and 3 in sensors_on_line and 4 in sensors_on_line:  # Right downer corner.
                motors.turn(-45, baseSpeed)
            elif 0 in sensors_on_line and 7 in sensors_on_line and 6 in sensors_on_line:  # Left upper corner.
                motors.turn(135, baseSpeed)
            elif 0 in sensors_on_line and 1 in sensors_on_line and 2 in sensors_on_line:  # Right upper corner.
                motors.turn(-135, baseSpeed)
            elif 6 in sensors_on_line and (7 in sensors_on_line or 5 in sensors_on_line):  # Line on the left.
                motors.turn(90, baseSpeed)
            elif 0 in sensors_on_line and (7 in sensors_on_line or 1 in sensors_on_line):  # Line on the right.
                motors.turn(-90, baseSpeed)
            elif 4 in sensors_on_line and (5 in sensors_on_line or 3 in sensors_on_line):  # Line on the back.
                motors.turn(180, baseSpeed)
            elif 2 in sensors_on_line and (1 in sensors_on_line or 3 in sensors_on_line):  # Line on the front.
                motors.turn(180, baseSpeed)

            if 1 in sensors_on_line:
                motors.backward(baseSpeed)
                sleep(0.3)
                motors.brake()
                print('left')
                motors.turn(-60.0, baseSpeed)
            elif 0 or 7 in sensors_on_line:
                motors.backward(baseSpeed)
                sleep(0.3)
                motors.brake()
                print('right')
                motors.turn(60.0, baseSpeed)
            elif 3 or 5 in sensors_on_line:
                motors.forward(baseSpeed)
                sleep(0.2)

            if 2 or 4 in sensors_on_line:
                if 1 in previousLine or 0 in previousLine or 7 in previousLine:
                    motors.backward(baseSpeed)

            previousLine = sensors_on_line
            # onLineLED.off()

        if 0 in obstacles:
            # if 2 in obstacles:
            #     motors.turn(-90, baseSpeed)
            # elif 4 in obstacles:
            #     motors.turn(90, baseSpeed)
            # else:
            motors.turn(-90, baseSpeed)
        elif 1 in obstacles:
            motors.turn(-45, baseSpeed)
        elif 3 in obstacles:
            motors.turn(45, baseSpeed)
        # elif 2 in obstacles:
        #     fire_after_obstacle('right')
        # elif 4 in obstacles:
        #     fire_after_obstacle('left')
        else:
            motors.forward(baseSpeed)

    except Exception as e:
        thermal_camera.close()
        print(e)
        break
