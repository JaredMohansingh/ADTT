import   cv2



############# CAMERA SETUP##############
capw = cv2.VideoCapture( 4 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

capb = cv2.VideoCapture( 2 ) 
capb.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capb.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not capw.isOpened():

    print("Cannot open camera")
    exit()

if not capb.isOpened():

    print("Cannot open camera")
    exit()
############# CAMERA SETUP##############


ret, framew = capw.read()
ret, frameb = capb.read()

while True:

    ret, framew = capw.read()
    ret, frameb = capb.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    framew = cv2.circle(framew.copy(), (640,10), 1, ( 255, 0,0), 5)
    frameb = cv2.circle(frameb.copy(), (640,10), 1, ( 255, 0,0), 5)
    
    framew = cv2.line(framew.copy(), (640,1), (640,720), (255, 0,0), 1)
    frameb = cv2.line(frameb.copy(), (640,1), (640,720), ( 255, 0,0), 1) 

    concat = cv2.hconcat([framew, frameb]) 

   
    cv2.imshow("image",concat)
    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
capb.release()
cv2.destroyAllWindows()