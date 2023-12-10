import   cv2, numpy as np
import time


############# CAMERA SETUP##############
capw = cv2.VideoCapture( 0 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


#capb = cv2.VideoCapture( 2 )  
#capb.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#capb.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#capb.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


if not capw.isOpened():

    print("Cannot open camera double U")
    exit()

#if not capb.isOpened():

#    print("Cannot open camera BEE")
#    exit()
############# CAMERA SETUP##############
 

ret, framew = capw.read()
#ret, frameb = capb.read()

fifth_w = framew
fourth_w = framew
third_w = framew
second_w = framew
first_w = framew
avg = framew
true_avg = framew
#time.sleep(5)
count = 0
while True: 

    ret, framew = capw.read()
    #ret, frameb = capb.read()
    #print(frameb.shape)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    cv2.imshow('video', framew)
    #cv2.imshow('video', frameb)
    #cv2.imshow('video', concat)
    
    #fifth_w = fourth_w
    #fourth_w = third_w

    third_w = second_w
    second_w = first_w
    first_w = framew
    true_avg = (((first_w)+(second_w)+(third_w))/(3))

    for x in range(720):
        for y in range(1280):
            true_avg_pix = true_avg[x,y]
            current_pix = framew[x,y]
            if ((true_avg_pix.all) == (current_pix.all)):
                avg[x,y] = [0,0,0]
            else :
                avg[x,y] = [1,1,1]


    cv2.imshow('video', avg)
    #cv2.imwrite("making_a_dataset/ovh/Wovh_"+str(count)+".jpeg", frameb)
    #cv2.imwrite("making_a_dataset/ovh/Bovh_"+str(count)+".jpeg", framew) 
    #count = count +1
    if cv2.waitKey(1) == ord('0'):
        break



    #time.sleep(5)
# When everything done, release the capture

capw.release()
#capb.release()
cv2.destroyAllWindows()