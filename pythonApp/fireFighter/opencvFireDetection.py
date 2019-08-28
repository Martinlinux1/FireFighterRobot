import cv2
import numpy as np

image = cv2.imread('fire_1.JPG')
cv2.imshow('image_original', image)

# image = cv2.resize(image, (1366, 768))

imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = [7, 140, 140]
upper = [17, 255, 255]
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")
mask = cv2.inRange(imageHSV, lower, upper)

output = cv2.bitwise_and(image, imageHSV, mask=mask)
cv2.imshow('mask', mask)

fire_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
template = cv2.imread('fire_template.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(fire_gray, template, cv2.TM_CCORR)
print(res)
threshold = 0.8
loc = np.where(res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    print(pt)

cv2.imshow('fire', image)

cv2.waitKey()
cv2.destroyAllWindows()
