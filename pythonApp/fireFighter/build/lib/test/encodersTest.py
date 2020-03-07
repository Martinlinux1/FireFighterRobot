import serial
import communicationHandler
import encoders
import hardwarehandler


def encoders_reading():
    hardwarehandler.update_encoders()


serial_port = serial.Serial("/dev/ttyUSB0", 115200)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
encoders = encoders.Encoders(comm_handler)

hardwarehandler = hardwarehandler.HardwareHandler(None, None, encoders)

while True:
    print(hardwarehandler.get_encoders())
