import cv2
import numpy as np

img = np.zeros([255, 255, 3], np.uint8)

image = cv2.rectangle(img, (0, 0), (124, 124), (255, 0, 0))

cv2.imshow("ok", img)
cv2.waitKey(0)
cv2.destroyAllWindows()