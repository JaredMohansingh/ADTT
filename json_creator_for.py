import json, os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from skimage.measure import label, regionprops, find_contours
from visualize import visualize
import  sys

real = 568
def mouse_point(event,x,y,flags,params):
    global take
    if event == cv2.EVENT_LBUTTONDOWN:
        take.append((x,y))
    

for iter in range(5000):

    take = []
    bbox = []

    sub_path = "making_a_dataset/5/Image"
    image_number = str(iter)
    image_path = sub_path+ image_number + ".jpg"
    if not os.path.isfile(image_path):
        continue
    
    image = cv2.imread(image_path)
    cv2.imwrite('making_a_dataset/train/Images/Image' + str(real) + '.jpg', image)

    cv2.imshow("Image", image)

    cv2.setMouseCallback("Image",mouse_point)
    cv2.waitKey(0)
    image = cv2.rectangle(image, take[0], take[1], (0, 255, 0), 1)

    bbox.append(take[0])
    bbox.append(take[1])
    take = []

    cv2.imshow("Image",image)

    cv2.setMouseCallback("Image",mouse_point)
    cv2.waitKey(0)
    image = cv2.circle(image, take[0], 1, (0, 255, 0), 1)
    image = cv2.circle(image, take[1], 1, (0, 255, 0), 1)

    bbox.append(take[0])
    bbox.append(take[1])
    cv2.imwrite('making_a_dataset/train/Examine/Image' + str(real) + '.jpg', image)


    image_info = {"bboxes":[[ bbox[0][0] , bbox[0][1] , bbox[1][0] , bbox[1][1] ]], "keypoints":[[[ bbox[2][0] , bbox[2][1] ,1],[ bbox[3][0]  , bbox[3][1] , 1]]]}

   
    json_info = json.dumps(image_info)
    json_File = open('making_a_dataset/train/Annotations/Image' + str(real) + '.json' ,'w')
    json_File.write(json_info)
    json_File.close()
    real = real +1