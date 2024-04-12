import   cv2
import numpy as np
import time



#This file is used to align the real world cameras with the ground markers and the overaly to ensure they are at the correct predetermined world coordinates


############# CAMERA SETUP##############
capw = cv2.VideoCapture( 2 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

if not capw.isOpened():

    print("Cannot open camera double U")
    exit()


ret, framew = capw.read()

############# CAMERA SETUP##############

while True:

    ret, framew = capw.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    

    r_image = cv2.rotate(framew, cv2.ROTATE_90_CLOCKWISE)
    


    cv2.imshow("image",r_image)
    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
cv2.destroyAllWindows()