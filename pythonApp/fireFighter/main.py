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

    def run(self):
        while self.is_alive():
            ir = cam.read_camera()

            if 0 in ir:
                print("camera reading failure")
            else:
                print("camera reading successful")
            camera_data_read_event.set()


class LightSensorsReader(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock

    def run(self) -> None:
        global light_sensors

        while True:
            light_values = []
            for i in range(8):
                self.lock.acquire()
                light_values.append(commHandler.get_light_sensor_data(i))
                self.lock.release()
            light_sensors = light_values


class DistanceSensorsReader(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock

    def run(self) -> None:
        global distance_sensors

        while True:
            distance_values = []
            for i in range(5):
                self.lock.acquire()
                distance_values.append(commHandler.get_distance_sensor_data(i))
                self.lock.release()
            distance_sensors = distance_values


class IMUSensorReader(threading.Thread):
    def __init__(self, lock):
        threading.Thread.__init__(self)
        self.lock = lock

    def run(self) -> None:
        global imu_sensor

        while True:
            self.lock.acquire()
            imu_sensor = commHandler.get_imu_sensor_data()
            self.lock.release()


def is_line():
    on_line_sensors = []
    for i in range(8):
        light_data = commHandler.get_light_sensor_data(i)
        if light_data > lightSensorsBlack:
            on_line_sensors.append(i)

    return on_line_sensors


def is_obstacle():
    sensors_detected = []

    for i in range(5):
        distance_data = commHandler.get_distance_sensor_data(i)
        if not distance_data:
            sensors_detected.append(i)

    return sensors_detected


def fire_after_obstacle(direction: str):
    if direction == 'right':
        obstacles = is_obstacle()
        while 2 in obstacles:
            motors.forward(baseSpeed)
        sleep(0.2)
        motors.brake()
        motors.turn(90, baseSpeed)
        motors.forward(baseSpeed)
        sleep(0.3)

    if direction == 'left':
        obstacles = is_obstacle()
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

# thermal_camera = pyusb2fir.USB2FIR(refreshRate=5)
serialPort = serial.Serial("/dev/ttyUSB0", 115200)

serial_lock = threading.Lock()

t1 = CameraFetcher()
t1.daemon = True

t2 = LightSensorsReader(serial_lock)
t2.daemon = True

t3 = DistanceSensorsReader(serial_lock)
t3.daemon = True

t4 = IMUSensorReader(serial_lock)
t4.daemon = True

# cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort)
motors = motorController.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.

light_sensors = []
distance_sensors = []
imu_sensor = -999

baseSpeed = 150

lightSensorsBlack = 300

previousLine = []
print('Light sensors calibration in 2 seconds...')
sleep(2)
print('calibrating light sensors...')
commHandler.calibrate_light_sensors()
print('DONE.')
t1.start()
t2.start()
t3.start()
t4.start()

while True:
    try:
        camera_data_read_event.wait()
        fire_coordinates = cam.is_fire(40)
        camera_data_read_event.clear()

        line = is_line()
        obstacles = is_obstacle()

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
            sensors_on_line = is_line()
            if max_fire_angle[0] < 15 and 0 in sensors_on_line:
                print("Extinguishing")
                motors.brake()
                servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)

                servo.value = servo_angle
                fan.on()
                sleep(5)
                fan.off()

                turned = False
        elif line:
            print('line')

            if 6 in line and 5 in line and 4 in line:                   # Left downer corner.
                motors.turn(45, baseSpeed)
                motors.forward(baseSpeed)
            elif 2 in line and 3 in line and 4 in line:                 # Right downer corner.
                motors.turn(-45, baseSpeed)
            elif 0 in line and 7 in line and 6 in line:                 # Left upper corner.
                motors.turn(135, baseSpeed)
            elif 0 in line and 1 in line and 2 in line:                 # Right upper corner.
                motors.turn(-135, baseSpeed)
            elif 6 in line and (7 in line or 5 in line):                # Line on the left.
                motors.turn(90, baseSpeed)
            elif 0 in line and (7 in line or 1 in line):                # Line on the right.
                motors.turn(-90, baseSpeed)
            elif 4 in line and (5 in line or 3 in line):                # Line on the back.
                motors.turn(180, baseSpeed)
            elif 2 in line and (1 in line or 3 in line):                # Line on the front.
                motors.turn(180, baseSpeed)

            if 1 in line:
                motors.backward(baseSpeed)
                sleep(0.3)
                motors.brake()
                print('left')
                motors.turn(-60.0, baseSpeed)
            elif 0 or 7 in line:
                motors.backward(baseSpeed)
                sleep(0.3)
                motors.brake()
                print('right')
                motors.turn(60.0, baseSpeed)
            elif 3 or 5 in line:
                motors.forward(baseSpeed)
                sleep(0.2)

            if 2 or 4 in line:
                if 1 in line or 0 in line or 7 in line:
                    motors.backward(baseSpeed)

            previousLine = line

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
