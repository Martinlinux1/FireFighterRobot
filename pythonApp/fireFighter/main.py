import cv2
from haarCascadeFireDetection import HaarCascadeFireDetection


fire_detector = HaarCascadeFireDetection('fire_detection.xml')
img = cv2.imread('fire_2.jpg')
fires = fire_detector.detect_fire(img)

for (x, y, w, h) in fires:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    roi_color = img[y:y + h, x:x + w]

cv2.imshow('img', img)
cv2.waitKey()
cv2.destroyAllWindows()
