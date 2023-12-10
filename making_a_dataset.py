import   cv2, numpy as np
import time


############# CAMERA SETUP##############
capw = cv2.VideoCapture( 0 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


capb = cv2.VideoCapture(2 ) 
capb.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capb.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capb.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


if not capw.isOpened():

    print("Cannot open camera double U")
    exit()

#if not capb.isOpened():

#    print("Cannot open camera BEE")
#    exit()
############# CAMERA SETUP##############
 

ret, framew = capw.read()
ret, frameb = capb.read()
#time.sleep(5)
count = 0
while True: 

    ret, framew = capw.read()
    ret, frameb = capb.read()
    #print(frameb.shape)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    

    #cv2.imshow('video', framew)
    #cv2.imshow('video', frameb)
    #cv2.imshow('video', concat)
    
    cv2.imwrite("making_a_dataset/ovh3/Wovh_"+str(count)+".jpeg", frameb)
    cv2.imwrite("making_a_dataset/ovh3/Bovh_"+str(count)+".jpeg", framew) 
    count = count +1
    if cv2.waitKey(1) == ord('0'):
        break
    time.sleep(2)
# When everything done, release the capture

capw.release()
#capb.release()
cv2.destroyAllWindows()