import serial
import multiprocessing
from IO import commiface, encodersiface
from handlers import encoders_handler


def encoders_reading():
    while True:
        enc_handler.update()


serial_port = serial.Serial("/dev/ttyUSB0", 115200)
comm_handler = commiface.CommInterface(serial_port)
encoders = encodersiface.EncodersInterface(comm_handler)

enc_handler = encoders_handler.EncodersHandler(encoders)
p1 = multiprocessing.Process(target=encoders_reading)
p1.daemon = True
p1.start()

while True:
    encoders_data = enc_handler.get()

    if not (encoders_data is None):
        print(encoders_data)
