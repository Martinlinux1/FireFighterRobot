from time import sleep

import serial

import communicationHandler
import hardwarehandler
import motorController
import motorsWriter
import sensorsReader


serial_port = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.05)

comm_handler = communicationHandler.CommunicationHandler(serial_port)

sensors_reader = sensorsReader.SensorsReader(comm_handler)
motors_writer = motorsWriter.MotorsWriter(comm_handler)

hardware_handler: hardwarehandler.HardwareHandler = hardwarehandler.HardwareHandler(sensors_reader, motors_writer)

motors = motorController.MotorController(hardware_handler, 0.05)

while True:
    motors.backward(255)
    hardware_handler.update_motors()
    sleep(5)
    motors.forward(255)
    hardware_handler.update_motors()
    sleep(5)

