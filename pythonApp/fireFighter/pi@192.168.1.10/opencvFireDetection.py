import cv2
import numpy as np

image = cv2.imread('fire_4.jpg')
cv2.imshow('image_original', image)

# image = cv2.resize(image, (1366, 768))

imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = [7, 140, 140]
upper = [17, 255, 255]
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")
mask = cv2.inRange(imageHSV, lower, upper)

color_output = cv2.bitwise_and(image, imageHSV, mask=mask)

cv2.imshow('mask', color_output)

fire_cascade = cv2.CascadeClassifier('fire_cascade.xml')

color_filter_gray = cv2.cvtColor(color_output, cv2.COLOR_BGR2GRAY)

fires = fire_cascade.detectMultiScale(color_filter_gray)

for (x, y, w, h) in fires:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 0), 2)


cv2.imshow('img', image)

cv2.waitKey()
cv2.destroyAllWindows()
