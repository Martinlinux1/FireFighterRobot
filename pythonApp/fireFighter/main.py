import threading
from time import sleep

import numpy as np
import serial

import communication
import communicationHandler
import motorController


# from gpiozero import DigitalOutputDevice
# from gpiozero import Servo


class CameraFetcher(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        global temperatures
        while self.is_alive():
            temperatures = cam.read_camera()

            if 0 in temperatures:
                pass
                print("camera reading failure")
            else:
                pass
                print("camera reading successful")


def robot_logic(motors):
    while True:
        try:
            sensors_on_line = np.ones(8)
            obstacles = np.ones(5)
            # fire_coordinates = cam.is_fire(temperatures=temperatures, threshold=40)
            #
            # if fire_coordinates[0]:
            #     print("Fire on: ", fire_coordinates)
            #
            #     all_fire_angles = cam.coordinates_to_angle(fire_coordinates[1])
            #
            #     print("Robot needs to turn: ", all_fire_angles)
            #
            #     max_val = [0, 0, 0]
            #     for i in fire_coordinates[1]:
            #         if i[2] > max_val[2]:
            #             max_val = i
            #
            #     print("Fire closest to robot: ", max_val)
            #     max_fire_angle = CameraReader.coordinates_to_angle(fire_coordinates)
            #
            #     print("Robot turning: ", max_fire_angle)
            #
            #     if max_fire_angle[0] > 30 or max_fire_angle[0] < -30:
            #         if max_fire_angle[0] > 0:
            #             motors.turn_manual('L', baseSpeed)
            #         else:
            #             motors.turn_manual('R', baseSpeed)
            #     else:
            #         pass
            #         motors.slide(max_fire_angle[0] * -1, baseSpeed)
            #
            #     if max_fire_angle[0] < 15 and 0 in sensors_on_line:
            #         print("Extinguishing")
            #         motors.brake()
            #         servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)
            #
            #         # servo.value = servo_angle
            #         # fan.on()
            #
            #         turned = False
            if 'a' == 'b':
                print('line')
                if 1 in sensors_on_line:
                    sleep(0.5)
                    # motors.backward(baseSpeed)
                    # motors.brake()
                    # print('left')
                    # motors.turn(-60.0, baseSpeed)
                elif 0 or 7 in sensors_on_line:
                    sleep(0.5)
                    # buzzer.on()
                    # motors.backward(baseSpeed)
                    # motors.brake()
                    # print('right')
                    # motors.turn(60.0, baseSpeed)
                elif 3 or 5 in sensors_on_line:
                    sleep(0.2)
                    # buzzer.on()
                    # motors.forward(baseSpeed)

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
            else:
                motors.forward(baseSpeed)

        except Exception as e:
            raise e


def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data[i] > lightSensorsBlack:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data[i]:
            sensors_detected.append(i)

    return sensors_detected


turned = False
fanPin = 4

# fan = DigitalOutputDevice(fanPin, False)
# buzzer = DigitalOutputDevice(15)
# servo = Servo(14)

# camera = usb2fir.USB2FIR(refreshRate=5)
serialPort = serial.Serial("/dev/ttyUSB0", 115200, timeout=0.05)

t = CameraFetcher()
t.daemon = True

# cam = CameraReader(camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
communication = communication.Communication(commHandler)
motors_controller = motorController.MotorController(communication, 0.05)  # Adjust the brake delay for your motor.

t2 = threading.Thread(target=robot_logic, args=[motors_controller])
t2.daemon = True
# temperatures = camera.initializeFrame()

baseSpeed = 100

lightSensorsBlack = 1400

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)

line_sensors = []
distance_sensors = []
imu_sensor = -999

motors_speed = []

t.start()
t2.start()

turn_delay_time = 0.1

while True:
    communication.update_sensors()
    # communication.update_motors()
    print(communication.get_light_sensors(), communication.get_distance_sensors(), communication.get_imu_sensor())
