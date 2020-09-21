from time import sleep

import serial

from IO import commiface, sensorsreader, motorswriter
from handlers import motors_handler
from motors import motors_controller

serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

comm_handler = commiface.CommInterface(serial_port)

sensors_reader = sensorsreader.SensorsReader(comm_handler)
motors_writer = motorswriter.MotorsWriter(comm_handler)

motors_handler = motors_handler.MotorsHandler(motors_writer)
motors = motors_controller.MotorController(motors_handler, 0.05)

while True:
    motors.backward(255)
    motors_handler.update()
    sleep(5)
    motors.forward(255)
    motors_handler.update()
    sleep(5)

