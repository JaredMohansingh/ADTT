import   cv2
import numpy as np
import time




image = cv2.imread('ADTT/overlay.jpg')


cv2.line(image, (0,360), (1280,360), (0,0,255))
cv2.line(image, (670,0), (670,720), (0,0,255))

cv2.line(image, (506,0), (506,720), (0,0,255))
cv2.line(image, (813,0), (813,720), (0,0,255))

cv2.line(image, (0,108), (1280,230), (0,0,255))
cv2.line(image, (0,612), (1280,490), (0,0,255))

rimage = cv2.rotate(image, cv2.ROTATE_180)
cv2.imshow("image", rimage)

cv2.waitKey(0)


cv2.destroyAllWindows()