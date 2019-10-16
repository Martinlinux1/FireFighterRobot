import threading
import time
from time import sleep

import numpy as np
import serial
from gpiozero import DigitalOutputDevice
from gpiozero import Servo

import communicationHandler
import motorController
from MathUtils import MathUtils
from cameraReader import CameraReader
from pyUSB2FIR.pyusb2fir import usb2fir


# Camera reader
class CameraFetcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global temperatures
        while self.is_alive():
            ir = [0]
            # ir = cam.read_camera()

            if 0 in ir:
                pass
                # print("camera reading failure")
            else:
                pass
                # print("camera reading successful")


def robot_logic():
    global line_sensors
    global distance_sensors
    global imu_sensor
    global previousLine
    global turned
    global baseSpeed
    global temperatures

    while True:
        # try:
        fire_coordinates = cam.is_fire(temperatures, threshold=40)

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

                turned = False
        elif sensors_on_line:
            print('line')

            # if 6 in line and 5 in line and 4 in line:  # Left downer corner.
            #     motors.slide(45, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(45, baseSpeed)
            # elif 2 in line and 3 in line and 4 in line:  # Right downer corner.
            #     motors.slide(-45, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(-45, baseSpeed)
            # elif 0 in line and 7 in line and 6 in line:  # Left upper corner.
            #     motors.slide(135, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(135, baseSpeed)
            # elif 0 in line and 1 in line and 2 in line:  # Right upper corner.
            #     motors.slide(-135, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(-135, baseSpeed)
            # elif 6 in line and (7 in line or 5 in line):  # Line on the left.
            #     motors.slide(90, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(90, baseSpeed)
            # elif 0 in line and (7 in line or 1 in line):  # Line on the right.
            #     motors.slide(-90, baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(-90, baseSpeed)
            # elif 4 in line and (5 in line or 3 in line):  # Line on the back.
            #     motors.forward(baseSpeed)
            # elif 2 in line and (1 in line or 3 in line):  # Line on the front.
            #     motors.backward(baseSpeed)
            #     sleep(turn_delay_time)
            #     motors.turn(180, baseSpeed)
            if 1 in sensors_on_line:
                motors.backward(baseSpeed)
                sleep(0.5)
                motors.brake()
                # print('left')
                motors.turn(-60.0, baseSpeed)
            elif 0 or 7 in sensors_on_line:
                buzzer.on()
                motors.backward(baseSpeed)
                sleep(0.5)
                motors.brake()
                # print('right')
                motors.turn(60.0, baseSpeed)
            elif 3 or 5 in sensors_on_line:
                buzzer.on()
                motors.forward(baseSpeed)
                sleep(0.2)

            previousLine = sensors_on_line
            buzzer.off()

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
            time_start = time.time()
            motors.forward(baseSpeed)
            time_elapsed = time.time() - time_start
            print(time_elapsed * 1000)

        # except Exception as e:
        #     thermal_camera.close()
        #     print(e)
        #     break


def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data > lightSensorsBlack:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data:
            sensors_detected.append(i)

    return sensors_detected


camera_data_read_event = threading.Event()

turned = False
fanPin = 4

fan = DigitalOutputDevice(fanPin, False)
buzzer = DigitalOutputDevice(15)
servo = Servo(14)

thermal_camera = usb2fir.USB2FIR(refreshRate=5)
serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

t = CameraFetcher()
t.daemon = True

cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.

temperatures = thermal_camera.initializeFrame()

baseSpeed = 100

lightSensorsBlack = 1400

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)

line_sensors = np.ones(8)
distance_sensors = np.ones(5)
imu_sensor = -999

sensors_on_line = []
obstacles = []

t.start()

turn_delay_time = 0.1

while True:
    for i in range(8):
        line_sensors[i] = commHandler.get_light_sensor_data(i)

        if i < 5:
            distance_sensors[i] = commHandler.get_distance_sensor_data(i)

    imu_sensor = commHandler.get_imu_sensor_data()

    sensors_on_line = is_line(line_sensors)
    obstacles = is_obstacle(distance_sensors)
