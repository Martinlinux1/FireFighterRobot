import cv2


class HaarCascadeFireDetection:
    def __init__(self, cascade_classifier):
        self.fire_cascade = cv2.CascadeClassifier(cascade_classifier)

    def detect_fire(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        fire = self.fire_cascade.detectMultiScale(img, 1.2, 5)
        print(fire)
        fire_coordinates = []

        for (x, y, w, h) in fire:
            fire_coordinates.append([x, y, w, h])

        return fire_coordinates
