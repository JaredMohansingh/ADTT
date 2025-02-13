import   cv2
import numpy as np
import time



#This file is used to align the real world cameras with the ground markers and the overaly to ensure they are at the correct predetermined world coordinates


############# CAMERA SETUP##############
capw = cv2.VideoCapture(  0 +cv2.CAP_DSHOW ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

capb = cv2.VideoCapture(  1 +cv2.CAP_DSHOW )  
capb.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capb.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capb.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

if not capw.isOpened():

    print("Cannot open camera double U")
    exit()

ret, framew = capw.read()

if not capb.isOpened():

    print("Cannot open camera BEE")
    exit()

ret, framew = capw.read()
ret, frameb = capb.read()



############# CAMERA SETUP##############

while True:

    ret, framew = capw.read()
    ret, frameb = capb.read()
    
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    concat = cv2.vconcat([frameb, framew])
    concat = cv2.rotate(concat, cv2.ROTATE_90_CLOCKWISE)

    #######################WALL#############################
    #Longways
    cv2.line(concat, (360,0), (360,1280), (0,0,255))
    cv2.line(concat, (195,0), (40,1280), (0,0,255))
    cv2.line(concat, (525,0), (680,1280), (0,0,255))
    #Sideways
    cv2.line(concat, (0,507), (720,507), (0,0,0))
    cv2.line(concat, (0,697), (720,697), (255,255,255))
    cv2.line(concat, (0,930), (720,930), (0,0,255))
    #######################WALL#############################

    #######################BEAM#############################
    #Longways
    cv2.line(concat, (1080,0), (1080,1280), (0,0,255))
    cv2.line(concat, (915,0), (760,1280), (0,0,255))
    cv2.line(concat, (1245,0), (1400,1280), (0,0,255))
    #Sideways
    cv2.line(concat, (720,529), (1440,529), (255,255,255))
    cv2.line(concat, (720,724), (1440,724), (0,0,0))
    cv2.line(concat, (720,961), (1440,961), (0,0,255))
    ########################BEAM#############################
   

    ##These lines overlay the ideal crosshair calibration from unity
 
    cv2.imshow("image",concat)
    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
capb.release()
cv2.destroyAllWindows()