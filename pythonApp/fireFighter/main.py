import threading
import test.fakeCamera
from pyusb2fir import USB2FIR
import cameraReader
from time import sleep


def camera_fetcher():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        x = cam.read_camera()


thermal_camera = test.fakeCamera.FakeCamera(4, 60)
cam = cameraReader.CameraReader(thermal_camera)
t = threading.Thread(target=camera_fetcher)
t.daemon = True
t.start()

while True:
    fire_coordinates = cam.is_fire(60)
    if fire_coordinates[0]:
        print("Fire on: ", fire_coordinates)

        all_fire_angles = cam.coordinates_to_angle(fire_coordinates[1])

        print("Robot needs to turn: ", all_fire_angles)

        max_val = [0, 0, 0]
        for i in fire_coordinates[1]:
            if i[2] > max_val[2]:
                max_val = i

        print("Fire closest to robot: ", max_val)

        max_fire_angle = cam.coordinates_to_angle(max_val)

        print("Robot turning: ", max_fire_angle)

    sleep(0.5)
