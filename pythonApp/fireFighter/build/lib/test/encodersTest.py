import serial
from IO import commiface, encodersiface
from handlers import hardwarehandler


def encoders_reading():
    hardwarehandler.update_encoders()


serial_port = serial.Serial("/dev/ttyUSB0", 115200)
comm_handler = commiface.CommInterface(serial_port)
encoders = encodersiface.EncodersInterface(comm_handler)

hardwarehandler = hardwarehandler.HardwareHandler(None, None, encoders)

while True:
    print(hardwarehandler.get_encoders())
