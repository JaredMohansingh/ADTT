
import cv2
from intersection import find_intersection


take = []
W_object = []
B_object = []

def mouse_point(event,x,y,flags,params):
    global take
    if event == cv2.EVENT_LBUTTONDOWN:
        take.append((x,y))
    
###################
        
############# CAMERA SETUP##############
capw = cv2.VideoCapture( 0 ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

capb = cv2.VideoCapture( 2 )  
capb.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capb.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capb.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

if not capw.isOpened():

    print("Cannot open camera double U")
    exit()

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
    
    concat = cv2.vconcat([framew, frameb])
    
    r_image = cv2.rotate(concat, cv2.ROTATE_90_CLOCKWISE)
    

    cv2.imshow("Wall Image", r_image)
    cv2.setMouseCallback("Wall Image",mouse_point)
    
    if cv2.waitKey(1) == ord('0'):
        
        new_take = take[0][0]-720

        W_object =[ new_take,take[0][1] ]
        B_object = take[1]
        
        break

# When everything done, release the capture
capw.release()
capb.release()
cv2.destroyAllWindows()

d__angle_of_view = 55.0 
h_angle_of_view = 25.73 
v_angle_of_view = 49 
down_angle = -55.0 

image_width_px = 720 
image_height_px = 1280 

beam_cam = [-2.2 ,0 ,3.0]
# wall cam is facing forward , toward positive x values 
wall_cam = [ 2.2, 0, 3.0]
#beam cam is facing backwards , towards negative x values 
print(W_object)
print(B_object)
print(find_intersection(image_height_px, image_width_px, v_angle_of_view, down_angle,beam_cam, wall_cam , W_object , B_object) ) 