import serial
import multiprocessing
import communicationHandler
import encoders
import hardwarehandler


def encoders_reading():
    while True:
        hardwarehandler.update_encoders()


serial_port = serial.Serial("/dev/ttyUSB0", 115200)
comm_handler = communicationHandler.CommunicationHandler(serial_port)
encoders = encoders.Encoders(comm_handler)

hardwarehandler = hardwarehandler.HardwareHandler(None, None, encoders)
p1 = multiprocessing.Process(target=encoders_reading)
p1.daemon = True
p1.start()

while True:
    encoders_data = hardwarehandler.get_encoders()

    if not (encoders_data is None):
        print(encoders_data)
