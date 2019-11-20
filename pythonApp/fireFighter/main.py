import multiprocessing
import threading
from time import sleep

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

t = CameraFetcher(cam)
t.daemon = True
t.start()

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

    if fire_coordinates[0]:
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

    elif (0 in sensors_on_line) or (7 in sensors_on_line):
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, 60, base_speed)
    elif 1 in sensors_on_line:
        motors.backward(base_speed)
        sleep(0.1)
        turn(hardware_handler, -60, base_speed)
    elif 0 in obstacles:
        turn(hardware_handler, -90, base_speed)
    elif 1 in obstacles:
        turn(hardware_handler, -45, base_speed)
    elif 3 in obstacles:
        turn(hardware_handler, 45, base_speed)

    else:
        motors.forward(base_speed)
