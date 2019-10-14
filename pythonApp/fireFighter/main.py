import threading
from time import sleep

import serial

import communicationHandler
import motorController


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


class LineSensorsReader(threading.Thread):
    def __init__(self, communication_handler: communicationHandler.CommunicationHandler):
        threading.Thread.__init__(self)
        self._communication_handler = communication_handler

    def run(self) -> None:
        global sensors_on_line
        while True:
            line_detected_sensors = []

            for i in range(8):
                line_sensor_value = self._communication_handler.get_light_sensor_data(i)

                if line_sensor_value > lightSensorsBlack:
                    line_detected_sensors.append(i)

            sensors_on_line = line_detected_sensors


class DistanceSensorsReader(threading.Thread):
    def __init__(self, communication_handler: communicationHandler.CommunicationHandler):
        threading.Thread.__init__(self)
        self._communication_handler = communication_handler

    def run(self) -> None:
        global obstacles
        while True:
            sensors_detected = []
            for i in range(5):
                distance_sensor_value = self._communication_handler.get_distance_sensor_data(i)

                if not distance_sensor_value:
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
serialPort = serial.Serial("/dev/ttyUSB0", 921600)

lock = threading.Lock()

# cam = CameraReader(thermal_camera)
commHandler = communicationHandler.CommunicationHandler(serialPort, lock)
motors = motorController.MotorController(commHandler, 0.05)           # Adjust the brake delay for your motor.

t1 = CameraFetcher()
t1.daemon = True

t3 = LineSensorsReader(commHandler)
t3.daemon = True

t4 = DistanceSensorsReader(commHandler)
t4.daemon = True

baseSpeed = 150

lightSensorsBlack = 300

line_sensors = []
sensors_on_line = []
distance_sensors = []
obstacles = []
imu_sensor = -999
last_received_message = ''

t1.start()
t3.start()
t4.start()

previousLine = []

while True:
    print(sensors_on_line, obstacles)

while True:
    try:
        fire_coordinates = cam.is_fire(40)

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
                motors.slide(max_fire_angle[0] * -1, baseSpeed)
            if max_fire_angle[0] < 15 and 0 in sensors_on_line:
                print("Extinguishing")
                motors.brake()
                servo_angle = MathUtils.valmap(max_fire_angle[1], -40, 40, -1, 1)
                servo.value = servo_angle
                fan.on()

        elif line:
            print('line')

            if 1 in line:
                buzzer.on()
                motors.backward(baseSpeed)
                sleep(0.5)
                buzzer.off()
                motors.brake()
                # print('left')
                motors.turn(-60.0, baseSpeed)
            elif 0 or 7 in line:
                buzzer.on()
                motors.backward(baseSpeed)
                sleep(0.5)
                buzzer.off()
                motors.brake()
                # print('right')
                motors.turn(60.0, baseSpeed)
            elif 3 or 5 in line:
                motors.forward(baseSpeed)
                sleep(0.2)

            if 2 or 4 in line:
                if 1 in line or 0 in line or 7 in line:
                    motors.backward(baseSpeed)

            previousLine = line
            buzzer.off()

        if 0 in obstacles:
            motors.turn(-90, baseSpeed)
        elif 1 in obstacles:
            motors.turn(-45, baseSpeed)
        elif 3 in obstacles:
            motors.turn(45, baseSpeed)

        else:
            time_start = time.time()
            motors.forward(baseSpeed)
            time_elapsed = time.time() - time_start
            print(time_elapsed * 1000)

    except Exception as e:
        thermal_camera.close()
        raise e
