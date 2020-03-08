from pyusb2fir import USB2FIR
import multiprocessing
import cameraReader
from firefinder import FireFinder


def read_camera(cam_reader: cameraReader.CameraReader):
    while True:
        cam_reader.update_camera_data()


thermal_camera = USB2FIR()

camera_reader = cameraReader.CameraReader(thermal_camera)

p1 = multiprocessing.Process(target=read_camera, args=[camera_reader])
p1.daemon = True
p1.start()

while True:
    temperatures = camera_reader.get_camera_data()

    fire_coordinates = FireFinder.is_fire(temperatures, 40)

    fire_angle = FireFinder.coordinates_to_angle(fire_coordinates[1])

    print(fire_angle)
