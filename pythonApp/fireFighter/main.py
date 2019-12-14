import multiprocessing
import queue
from time import sleep, time

import serial
from gpiozero import DigitalOutputDevice, Servo
from pyusb2fir import USB2FIR

import cameraReader
import communicationHandler
import hardwarehandler
import motorController
import motorsWriter
import sensorsReader
from firefinder import FireFinder
from mathUtils import MathUtils


def read_camera(cam_reader: cameraReader.CameraReader):
    while True:
        cam_reader.update_camera_data()


# Updating robot data.
def robot_data_handler(c):
    while True:
        c.update_sensors()
        c.update_motors()


def find_max_fire(fire_coord):
    max_fire_coordinates = FireFinder.max_fire(fire_coord)
    max_fire_angle = FireFinder.coordinates_to_angle(max_fire_coordinates)

    return max_fire_angle


# Is line present on any line sensor.
def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data[i] > 2500:
            on_line_sensors.append(i)

    return on_line_sensors


# Is obstacle present on any obstacle sensor.
def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data[i]:
            sensors_detected.append(i)

    return sensors_detected


def extinguish_fire(fire_coord, line_detected, obstacles_detected):
    if fire_coord[0]:
        max_fire_angle = find_max_fire(fire_coord)

        if 0 in line_detected and 0 in obstacles_detected:
            print("Extinguishing")
            motors.brake()
            servo_angle = MathUtils.valmap(max_fire_angle[1], -90, 90, -1, 1)

            servo.value = servo_angle
            fan.on()
            sleep(5)
            fan.off()

            motors.backward(base_speed)
            sleep(1)
            print('Turning started')
            motors.turn(135, base_speed)

            print('Extinguishing done.')

            return True

    return False


# Finds fire and takes action.
def find_fire(fire_coord, sensors_line, obstacles_detected):
    if not extinguish_fire(fire_coord, sensors_line, obstacles_detected):
        if fire_coord[0]:
            while not extinguish_fire(fire_coord, sensors_line, obstacles_detected):
                sens = hardware_handler.get_sensors()
                temps = cam.get_camera_data()
                print(temps)
                try:
                    l_sensors = sens[0]
                    d_sensors = sens[1]
                except TypeError:
                    continue

                fire_coord = FireFinder.is_fire(temps, threshold=40)
                print(fire_coord)
                sensors_line = is_line(l_sensors)
                obstacles_detected = is_obstacle(d_sensors)

                max_fire_angle = find_max_fire(fire_coord)

                print("Robot turning: ", max_fire_angle)

                if max_fire_angle[0] > 20 or max_fire_angle[0] < -20:
                    motors.turn(max_fire_angle[0] * -1, base_speed - 20)
                else:
                    motors.slide(max_fire_angle[0] * -1, base_speed)

            print('fire extinguished')
            return True

    return False


# Avoids lines.
def avoid_line(fire_coord, sensors_line, obstacles_detected):
    if not extinguish_fire(fire_coord, sensors_line, obstacles_detected):
        if not line_history.empty():
            previous_line = line_history.get()
        else:
            previous_line = [0, 0]

        # Corner detection.
        if 7 in sensors_line and previous_line[0] == 1 and time() - previous_line[1] < 1:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-90, base_speed)
            line_history.put([1, time()])
            return True

        elif 1 in sensors_line and previous_line[0] == 7 and time() - previous_line[1] < 1:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(90, base_speed)
            line_history.put([7, time()])
            return True

        # Front sensor line detection.
        if 0 in sensors_on_line and previous_line[0] == 7:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(60, base_speed)

            line_history.put([7, time()])
            return True

        elif 0 in sensors_on_line and previous_line[0] == 1:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-60, base_speed)

            line_history.put([1, time()])
            return True

        elif 0 in sensors_on_line:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-60, base_speed)

            line_history.put([1, time()])

        # Detection of line in specific situations.
        if 6 in sensors_line and 5 in sensors_line and 4 in sensors_line:  # Left downer corner.
            motors.slide(45, base_speed)
            sleep(0.1)
            motors.turn(45, base_speed)
            return True

        elif 2 in sensors_line and 3 in sensors_line and 4 in sensors_line:  # Right downer corner.
            motors.slide(-45, base_speed)
            sleep(0.1)
            motors.turn(-45, base_speed)
            return True

        elif 0 in sensors_line and 7 in sensors_line and 6 in sensors_line:  # Left upper corner.
            motors.slide(135, base_speed)
            sleep(0.1)
            motors.turn(135, base_speed)
            return True

        elif 0 in sensors_line and 1 in sensors_line and 2 in sensors_line:  # Right upper corner.
            motors.slide(-135, base_speed)
            sleep(0.1)
            motors.turn(-135, base_speed)
            return True

        elif 6 in sensors_line and (7 in sensors_line or 5 in sensors_line):  # Line on the left.
            motors.slide(90, base_speed)
            sleep(0.1)
            motors.turn(90, base_speed)
            return True

        elif 0 in sensors_line and (7 in sensors_line or 1 in sensors_line):  # Line on the right.
            motors.slide(-90, base_speed)
            sleep(0.1)
            motors.turn(-90, base_speed)
            return True

        elif 4 in sensors_line and (5 in sensors_line or 3 in sensors_line):  # Line on the back.
            motors.forward(base_speed)
            return True

        elif 2 in sensors_line and (1 in sensors_line or 3 in sensors_line):  # Line on the front.
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(180, base_speed)
            return True

        # Normal sensors_line detection and avoiding.
        if 7 in sensors_line:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(60, base_speed)

            line_history.put([7, time()])
            return True

        elif 1 in sensors_line:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-60, base_speed)

            line_history.put([1, time()])
            return True

    # No line detected
    return False


# Avoids obstacles.
def avoid_obstacle(fire_coord, sensors_line, obstacles_detected):
    if not extinguish_fire(fire_coord, sensors_line, obstacles_detected):
        if 0 in obstacles_detected:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-90, base_speed)

            return True
        elif 1 in obstacles:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(-45, base_speed)

            return True
        elif 3 in obstacles:
            motors.backward(base_speed)
            sleep(0.1)
            motors.turn(45, base_speed)

            return True

    # No obstacle detected.
    return False


fan = DigitalOutputDevice(4, False)
servo = Servo(14)

thermal_camera = USB2FIR(refreshRate=3)
serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

cam = cameraReader.CameraReader(thermal_camera)
comm_handler = communicationHandler.CommunicationHandler(serial_port)

sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)

hardware_handler: hardwarehandler.HardwareHandler = hardwarehandler.HardwareHandler(sensors_reader, motors_writer)

motors = motorController.MotorController(hardware_handler, 0.05)

line_history = queue.Queue()

camera_reading_process = multiprocessing.Process(target=read_camera, args=[cam])
camera_reading_process.daemon = True
camera_reading_process.start()

robot_logic_process = multiprocessing.Process(target=robot_data_handler, args=[hardware_handler])
robot_logic_process.daemon = True
robot_logic_process.start()

base_speed = 100
sleep(5)
while True:
    sensors = hardware_handler.get_sensors()
    temperatures = cam.get_camera_data()
    print(temperatures)

    try:
        light_sensors = sensors[0]
        distance_sensors = sensors[1]
        imu_sensor = sensors[2]
    except TypeError:
        continue

    fire_coordinates = FireFinder.is_fire(temperatures, threshold=40)
    sensors_on_line = is_line(light_sensors)
    obstacles = is_obstacle(distance_sensors)

    print(sensors_on_line)
    print(obstacles)
    print(fire_coordinates)

    is_fire = find_fire(fire_coordinates, sensors_on_line, obstacles)

    any_line = avoid_line(fire_coordinates, sensors_on_line, obstacles)
    are_obstacles = avoid_obstacle(fire_coordinates, sensors_on_line, obstacles)

    if (not is_fire) and (not any_line) and (not are_obstacles):
        motors.forward(base_speed)
