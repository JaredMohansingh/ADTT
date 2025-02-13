import   cv2
import numpy as np
import time

#This file is used to generate the overlay for aligning the cameras to the ground markers for calibration

image = cv2.imread('ADTT/overlay.jpg',1)

#######################WALL#############################
#Longways
cv2.line(image, (360,0), (360,1280), (0,0,255))
cv2.line(image, (195,0), (40,1280), (0,0,255))
cv2.line(image, (525,0), (680,1280), (0,0,255))
#Sideways
cv2.line(image, (0,507), (720,507), (0,0,255))
cv2.line(image, (0,697), (720,697), (255,255,255))
cv2.line(image, (0,930), (720,930), (0,0,0))
#######################WALL#############################

#######################BEAM#############################
#Longways
cv2.line(image, (1080,0), (1080,1280), (0,0,255))
cv2.line(image, (915,0), (760,1280), (0,0,255))
cv2.line(image, (1245,0), (1400,1280), (0,0,255))
#Sideways
cv2.line(image, (720,529), (1440,529), (255,255,255))
cv2.line(image, (720,724), (1440,724), (0,0,0))
cv2.line(image, (720,961), (1440,961), (0,0,255))
########################BEAM#############################
cv2.imshow("image", image)

cv2.waitKey(0)


cv2.destroyAllWindows()