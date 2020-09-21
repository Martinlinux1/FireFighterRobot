import unittest
import threading

from camera import camera_reader
import camera.mock.mockCamera


def camera_fetcher():
    tc = threading.currentThread()
    while getattr(tc, "do_run", True):
        cam.update()


thermal_camera = camera.mock.mockCamera.MockCamera(4, 60)
cam = camera_reader.CameraReader(thermal_camera)
t = threading.Thread(target=camera_fetcher)
t.daemon = True
t.start()


class TestGet(unittest.TestCase):
    def test_get_successful(self):
        data = cam.get()
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
