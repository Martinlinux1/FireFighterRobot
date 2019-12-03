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


# Turn robot by a given angle.
def turn(handler: hardwarehandler.HardwareHandler, angle, speed):
    sensors_data = []

    while not sensors_data:
        sensors_data = handler.get_sensors()

    robot_angle = sensors_data[2]

    target_angle = robot_angle + angle
    target_angle = target_angle % 360

    print(robot_angle)
    print(angle)
    print(target_angle)

    if target_angle < 0:
        target_angle = target_angle + 360

    while True:
        sensors_data = []
        while not sensors_data:
            sensors_data = handler.get_sensors()
        robot_angle = sensors_data[2]

        diff = target_angle - robot_angle
        direction = 180 - (diff + 360) % 360

        if direction > 0:
            motors.right(speed)
        else:
            motors.left(speed)

        if abs(diff) < 5:
            motors.brake()
            return


def extinguish_fire(fire_coord, line_detected, obstacles_detected):
    global base_speed

    if fire_coord[0]:
        max_fire_angle = find_max_fire(fire_coord)

        if max_fire_angle[0] in range(-15, 15) and 0 in line_detected:
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
            turn(hardware_handler, 135, base_speed)

            print('Extinguishing done.')

            return True

    return False


# Finds fire and takes action.
def find_fire(camera, handler_hardware):
    global base_speed

    line_sensors = []
    obstacle_sensors = []

    while True:
        fire_data = camera.get_camera_data()
        print(fire_data)
        fire_coord = FireFinder.is_fire(fire_data, threshold=40)

        sensors_data = handler_hardware.get_sensors()

        try:
            line_sensors = is_line(sensors_data[0])
            obstacle_sensors = is_obstacle(sensors_data[1])
        except TypeError:
            pass

        if not extinguish_fire(fire_coord, line_sensors, obstacle_sensors):
            if fire_coord[0]:
                max_fire_angle = find_max_fire(fire_coord)

                print("Robot turning: ", max_fire_angle)

                if max_fire_angle[0] > 15 or max_fire_angle[0] < -15:
                    if max_fire_angle[0] > 0:
                        motors.left(base_speed)
                    else:
                        motors.right(base_speed)
                else:
                    motors.slide(max_fire_angle[0] * -1, base_speed)


# Avoids lines.
def avoid_line(handler_hardware):
    global base_speed

    line_history = queue.Queue()
    sensors_line = []

    while True:
        sensors_data = handler_hardware.get_sensors()
        try:
            sensors_line = is_line(sensors_data[0])
        except TypeError:
            pass

        if not line_history.empty():
            previous_line = line_history.get()
        else:
            previous_line = [0, 0]

        # Corner detection.
        if 7 in sensors_line and previous_line[0] == 1 and time() - previous_line[1] < 1:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -90, base_speed)
            line_history.put([1, time()])

        elif 1 in sensors_line and previous_line[0] == 7 and time() - previous_line[1] < 1:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, 90, base_speed)
            line_history.put([7, time()])

        # Front sensor line detection.
        if 0 in sensors_line and previous_line[0] == 7:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, 60, base_speed)

            line_history.put([7, time()])

        elif 0 in sensors_line and previous_line[0] == 1:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -60, base_speed)

            line_history.put([1, time()])

        elif 0 in sensors_line:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -60, base_speed)

            line_history.put([1, time()])

        # Detection of line in specific situations.
        if 6 in sensors_line and 5 in sensors_line and 4 in sensors_line:  # Left downer corner.
            motors.slide(45, base_speed)
            sleep(0.1)
            turn(hardware_handler, 45, base_speed)

        elif 2 in sensors_line and 3 in sensors_line and 4 in sensors_line:  # Right downer corner.
            motors.slide(-45, base_speed)
            sleep(0.1)
            turn(hardware_handler, -45, base_speed)

        elif 0 in sensors_line and 7 in sensors_line and 6 in sensors_line:  # Left upper corner.
            motors.slide(135, base_speed)
            sleep(0.1)
            turn(hardware_handler, 135, base_speed)

        elif 0 in sensors_line and 1 in sensors_line and 2 in sensors_line:  # Right upper corner.
            motors.slide(-135, base_speed)
            sleep(0.1)
            turn(hardware_handler, -135, base_speed)

        elif 6 in sensors_line and (7 in sensors_line or 5 in sensors_line):  # Line on the left.
            motors.slide(90, base_speed)
            sleep(0.1)
            turn(hardware_handler, 90, base_speed)

        elif 0 in sensors_line and (7 in sensors_line or 1 in sensors_line):  # Line on the right.
            motors.slide(-90, base_speed)
            sleep(0.1)
            turn(hardware_handler, -90, base_speed)

        elif 4 in sensors_line and (5 in sensors_line or 3 in sensors_line):  # Line on the back.
            motors.forward(base_speed)

        elif 2 in sensors_line and (1 in sensors_line or 3 in sensors_line):  # Line on the front.
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, 180, base_speed)

        # Normal sensors_line detection and avoiding.
        if 7 in sensors_line:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, 60, base_speed)

            line_history.put([7, time()])

        elif 1 in sensors_line:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -60, base_speed)

            line_history.put([1, time()])


# Avoids obstacles.
def avoid_obstacle(handler_hardware):
    global base_speed

    obstacles_detected = []
    while True:
        sensors_data = handler_hardware.get_sensors()

        try:
            obstacles_detected = is_obstacle(sensors_data[1])
        except TypeError:
            pass

        if 0 in obstacles_detected:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -90, base_speed)

        elif 1 in obstacles_detected:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, -45, base_speed)

        elif 3 in obstacles_detected:
            motors.backward(base_speed)
            sleep(0.1)
            turn(hardware_handler, 45, base_speed)


base_speed = 100

fan = DigitalOutputDevice(4, False)
servo = Servo(14)

thermal_camera = USB2FIR()
serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

cam = cameraReader.CameraReader(thermal_camera)
comm_handler = communicationHandler.CommunicationHandler(serial_port)

sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)

hardware_handler: hardwarehandler.HardwareHandler = hardwarehandler.HardwareHandler(sensors_reader, motors_writer)

motors = motorController.MotorController(hardware_handler, 0.05)

camera_reading_process = multiprocessing.Process(target=read_camera, args=[cam])
camera_reading_process.daemon = True
camera_reading_process.start()

robot_data_updater = multiprocessing.Process(target=robot_data_handler, args=[hardware_handler])
robot_data_updater.daemon = True
robot_data_updater.start()

fire_detected_event = multiprocessing.Event()
line_detected_event = multiprocessing.Event()
obstacle_detected_event = multiprocessing.Event()

fire_finder = multiprocessing.Process(target=find_fire, args=[cam, hardware_handler], daemon=True)
line_avoid = multiprocessing.Process(target=avoid_line, args=[hardware_handler], daemon=True)
obstacle_avoid = multiprocessing.Process(target=avoid_obstacle, args=[hardware_handler], daemon=True)

fire_finder.start()
line_avoid.start()
obstacle_avoid.start()

camera_reading_process.join()
robot_data_updater.join()
fire_finder.join()
line_avoid.join()
obstacle_avoid.join()
