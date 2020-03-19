import serial
from IO import communicationInterface, encodersInterface
from handlers import hardwarehandler


def encoders_reading():
    hardwarehandler.update_encoders()


serial_port = serial.Serial("/dev/ttyUSB0", 115200)
comm_handler = communicationInterface.CommunicationInterface(serial_port)
encoders = encodersInterface.EncodersInterface(comm_handler)

hardwarehandler = hardwarehandler.HardwareHandler(None, None, encoders)

while True:
    print(hardwarehandler.get_encoders())
