from test import fakeCamera
import  cameraReader
from time import sleep


thermal_camera = fakeCamera.FakeCamera(4, 49)
cam = cameraReader.CameraReader(thermal_camera)

sleep(2)

while True:
    fire_coordinates = cam.is_fire(50)
    if fire_coordinates[0]:
        print(fire_coordinates)
    sleep(0.5)

