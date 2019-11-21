import multiprocessing
import queue
import threading
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
from mathUtils import MathUtils


class CameraFetcher(threading.Thread):
    def __init__(self, thermal_camera: cameraReader.CameraReader):
        threading.Thread.__init__(self)
        self._thermal_camera = thermal_camera

    def run(self) -> None:
        while self.is_alive():
            ir = self._thermal_camera.read_camera()


def robot_data_handler(c):
    while True:
        c.update_sensors()
        c.update_motors()


def is_line(line_sensors_data):
    on_line_sensors = []
    for i in range(8):
        if line_sensors_data[i] > 2500:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle(distance_sensors_data):
    sensors_detected = []

    for i in range(5):
        if not distance_sensors_data[i]:
            sensors_detected.append(i)

    return sensors_detected


def turn(handler: hardwarehandler.HardwareHandler, angle, speed):
    sensors_data = []

    while not sensors_data:
        sensors_data = handler.get_sensors()

    robot_angle = sensors_data[2]

    target_angle = robot_angle + angle
    target_angle = target_angle % 360

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


def find_fire(fire_coord):
    if fire_coord[0]:
        print("Fire on: ", fire_coordinates)

        all_fire_angles = cameraReader.CameraReader.coordinates_to_angle(fire_coordinates[1])

        print("Robot needs to turn: ", all_fire_angles)

        max_fire_angle = cameraReader.CameraReader.coordinates_to_angle(fire_coordinates)

        print("Robot turning: ", max_fire_angle)

        if max_fire_angle[0] > 30 or max_fire_angle[0] < -30:
            if max_fire_angle[0] > 0:
                motors.left(base_speed)
            else:
                motors.right(base_speed)
        else:
            motors.slide(max_fire_angle[0] * -1, base_speed)

        if 0 in obstacles:
            print("Extinguishing")
            motors.brake()
            servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

            servo.value = servo_angle
            fan.on()
            sleep(5)
            fan.off()

            turned = False

        return True

    return False


def avoid_line(sensors_line):
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
        return True

    elif 1 in sensors_line and previous_line[0] == 7 and time() - previous_line[1] < 1:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, 90, base_speed)
        line_history.put([7, time()])
        return True

    # Front sensor line detection.
    if 0 in sensors_on_line and previous_line[0] == 7:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, 60, base_speed)

        line_history.put([7, time()])
        return True

    elif 0 in sensors_on_line and previous_line[0] == 1:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, -60, base_speed)

        line_history.put([1, time()])
        return True

    # Detection of line in specific situations.
    if 6 in sensors_line and 5 in sensors_line and 4 in sensors_line:  # Left downer corner.
        motors.slide(45, base_speed)
        sleep(0.5)
        turn(hardware_handler, 45, base_speed)
        return True

    elif 2 in sensors_line and 3 in sensors_line and 4 in sensors_line:  # Right downer corner.
        motors.slide(-45, base_speed)
        sleep(0.5)
        turn(hardware_handler, -45, base_speed)
        return True

    elif 0 in sensors_line and 7 in sensors_line and 6 in sensors_line:  # Left upper corner.
        motors.slide(135, base_speed)
        sleep(0.5)
        turn(hardware_handler, 135, base_speed)
        return True

    elif 0 in sensors_line and 1 in sensors_line and 2 in sensors_line:  # Right upper corner.
        motors.slide(-135, base_speed)
        sleep(0.5)
        turn(hardware_handler, -135, base_speed)
        return True

    elif 6 in sensors_line and (7 in sensors_line or 5 in sensors_line):  # Line on the left.
        motors.slide(90, base_speed)
        sleep(0.5)
        turn(hardware_handler, 90, base_speed)
        return True

    elif 0 in sensors_line and (7 in sensors_line or 1 in sensors_line):  # Line on the right.
        motors.slide(-90, base_speed)
        sleep(0.5)
        turn(hardware_handler, -90, base_speed)
        return True

    elif 4 in sensors_line and (5 in sensors_line or 3 in sensors_line):  # Line on the back.
        motors.forward(base_speed)
        return True

    elif 2 in sensors_line and (1 in sensors_line or 3 in sensors_line):  # Line on the front.
        motors.backward(base_speed)
        sleep(0.5)
        turn(hardware_handler, 180, base_speed)
        return True

    # Normal sensors_line detection and avoiding.
    if 7 in sensors_line:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, 60, base_speed)

        line_history.put([7, time()])
        return True

    elif 1 in sensors_line:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, -60, base_speed)

        line_history.put([1, time()])
        return True

    # No line detected
    return False


def avoid_obstacle(obstacles_detected):
    if 0 in obstacles_detected:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, -90, base_speed)

        return True
    elif 1 in obstacles:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, -45, base_speed)

        return True
    elif 3 in obstacles:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, 45, base_speed)

        return True

    # No obstacle detected.
    return False


fan = DigitalOutputDevice(4, False)
servo = Servo(14)

thermal_camera = USB2FIR(refreshRate=5)
serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

cam = cameraReader.CameraReader(thermal_camera)
comm_handler = communicationHandler.CommunicationHandler(serial_port)

sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)

hardware_handler: hardwarehandler.HardwareHandler = hardwarehandler.HardwareHandler(sensors_reader, motors_writer)

motors = motorController.MotorController(hardware_handler, 0.05)

line_history = queue.Queue()

# t = CameraFetcher(cam)
# t.daemon = True
# t.start()

robot_logic_process = multiprocessing.Process(target=robot_data_handler, args=[hardware_handler])
robot_logic_process.daemon = True
robot_logic_process.start()

base_speed = 100

while True:
    sensors = hardware_handler.get_sensors()

    try:
        light_sensors = sensors[0]
        distance_sensors = sensors[1]
        imu_sensor = sensors[2]
    except TypeError:
        continue

    fire_coordinates = cam.is_fire(threshold=40)
    sensors_on_line = is_line(light_sensors)
    obstacles = is_obstacle(distance_sensors)

    print(sensors_on_line)
    print(obstacles)
    print(fire_coordinates)

    # is_fire = find_fire(fire_coordinates)
    any_line = avoid_line(sensors_on_line)
    are_obstacles = avoid_obstacle(obstacles)

    if (not any_line) and (not are_obstacles):
        motors.forward(base_speed)
