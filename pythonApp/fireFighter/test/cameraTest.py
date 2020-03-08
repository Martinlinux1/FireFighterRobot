import threading

import cameraReader
import test.fakeCamera


def camera_fetcher():
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        x = cam.read_camera()
        print(x)


thermal_camera = test.fakeCamera.FakeCamera(4, 60)
cam = cameraReader.CameraReader(thermal_camera)
t = threading.Thread(target=camera_fetcher)
t.daemon = True
t.start()

while True:
    fire_coordinates = cam.is_fire(60)
    if fire_coordinates[0]:
        print("Fire on: ", fire_coordinates)

        all_fire_angles = cameraReader.CameraReader.coordinates_to_angle(fire_coordinates[1])

        print("Robot needs to turn: ", all_fire_angles)

        max_fire_angle = cameraReader.CameraReader.coordinates_to_angle(fire_coordinates)

        print("Robot turning: ", max_fire_angle)
