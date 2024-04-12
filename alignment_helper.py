import   cv2
import numpy as np
import time



#This file is used to align the real world cameras with the ground markers and the overaly to ensure they are at the correct predetermined world coordinates


############# CAMERA SETUP##############
capw = cv2.VideoCapture( 2 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

capb = cv2.VideoCapture( 0 )  
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
    

    cv2.line(framew, (0,360), (1280,360), (0,0,255))
    cv2.line(framew, (467,0), (467,720), (0,0,255))
    cv2.line(framew, (610,0), (610,720), (0,0,255))
    cv2.line(framew, (774,0), (774,720), (0,0,255))
    
    cv2.line(framew, (0,230), (1280,108), (0,0,255))
    cv2.line(framew, (0,490), (1280,612), (0,0,255))



    cv2.line(frameb, (0,360), (1280,360), (0,0,255))
    cv2.line(frameb, (467,0), (467,720), (0,0,255))
    cv2.line(frameb, (610,0), (610,720), (0,0,255))
    cv2.line(frameb, (774,0), (774,720), (0,0,255))
    
    cv2.line(frameb, (0,230), (1280,108), (0,0,255))
    cv2.line(frameb, (0,490), (1280,612), (0,0,255)) 
    

    concat = cv2.vconcat([framew, frameb])
    
    r_image = cv2.rotate(concat, cv2.ROTATE_90_CLOCKWISE)
    


    cv2.imshow("image",r_image)
    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
capb.release()
cv2.destroyAllWindows()