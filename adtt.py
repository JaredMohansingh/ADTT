import torch,  cv2, numpy as np
from torch.utils.data import  DataLoader
import torchvision
from NN.utils import collate_fn
from NN.datasetclass import  PredDataset
from NN.training import get_model
from NN.save_image import save_image
from intersection import find_intersection
from laser_aimer import find_az_and_theta
import serial
import time


#-----------------------------#INITIALISE#----------------------------------------------------------------------------------------------#

    #vvvvvvvvvvvv# CALIBRATE LASER #vvvvvvvvvvvvv#   

arduino_a = serial.Serial('/dev/ttyACM0', 9600) 
arduino_t = serial.Serial('/dev/ttyACM1', 9600) 
val_a = 0
val_t = 0
laser_on = "l"
laser_off = "n"
reset_sensor = "r"
jnt = "000"

time.sleep(2) # Give some time for the serial connection to establish

while(True):
    
    jnt  = input("Enter a for azimuth, enter t for theta, then u for up or d down , or just the angle / servo speed")

    if( jnt[0] == "X"):
        break

    if( jnt[0] == "a"):

        if ( jnt[1]== "r" ):
            arduino_a.write(reset_sensor.encode())
            val_a = 0 

        if (jnt[1] == "u"):
            val_a = val_a +45
            arduino_a.write(str(val_a ).encode()) 
        
        if (jnt[1] == "d"):
            val_a = val_a -45
            arduino_a.write(str(val_a ).encode()) 
        
        if (jnt[1:].isdigit()):
            val_a = float(jnt[1:])
            arduino_a.write(str(val_a ).encode()) 
        
    ################################################

    if( jnt[0] == "l"):
        arduino_t.write(laser_on.encode()) 
    if( jnt[0] == "n"):
        arduino_t.write(laser_off.encode()) 

    if( jnt[0] == "t"):

        if ( jnt[1]== "r" ):
          arduino_t.write(reset_sensor.encode())
          val_t = 0 

        if (jnt[1] == "u"):
          val_t = val_t +45
          arduino_t.write(str(val_t ).encode()) 
      
        if (jnt[1] == "d"):
          val_t = val_t -45
          arduino_t.write(str(val_t ).encode()) 
      
        if (jnt[1:].isdigit()):
          val_t = float(jnt[1:])
          arduino_t.write(str(val_t ).encode()) 
      
    print("Val a is  ")
    print(val_a)
    print(" ")
    print("Val t is ")
    print(val_t)
    print(" ")
    #^^^^^^^^^^^^# CALIBRATE LASER #^^^^^^^^^^^^#


    #vvvvvvvvvvvv# INTERSECTION #vvvvvvvvvvvvv#   

laser_posn = [0,0,3]

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
#default values

    #^^^^^^^^^^^^# INTERSECTION #^^^^^^^^^^^^#

    #vvvvvvvvvvvv# CAMERA SETUP #vvvvvvvvvvvvv#
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
    #^^^^^^^^^^^^# CAMERA SETUP #^^^^^^^^^^^^#  

    #vvvvvvvvvvvv# NN SETUP #vvvvvvvvvvvvv#
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'NN/pth_files/low_res_birds_80.pth')
model.to(device)

KEYPOINTS_FOLDER_TEST = 'NN/live_recongize'
    #^^^^^^^^^^^^# NN SETUP#^^^^^^^^^^^^#    

#-----------------------------#INITIALISE#----------------------------------------------------------------------------------------------#

#-----------------------------#MAIN  LOOP#----------------------------------------------------------------------------------------------#
while (True):

        #vvvvvvvvvvvv# TAKE PICTURES #vvvvvvvvvvvvv#

    ret, framew = capw.read()
    ret, frameb = capb.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    concat = cv2.hconcat([framew, frameb]) 
    cv2.imwrite("NN/live_recongize/Images/live.jpg", concat) 
        #^^^^^^^^^^^^# TAKE PICTURES #^^^^^^^^^^^^#

        #vvvvvvvvvvvv# RECONGIZING USING ML #vvvvvvvvvvvvv#
    dataset_test = PredDataset(KEYPOINTS_FOLDER_TEST, transform=None, demo=False)
    data_loader_test = DataLoader(dataset_test, batch_size=1, shuffle=False, collate_fn=collate_fn)
    iterator = iter(data_loader_test)
    images, targets = next(iterator)
    images = list(image.to(device) for image in images)

    with torch.no_grad():
        model.to(device)
        model.eval()
        output = model(images)

    image_w = (images[0].permute(1, 2, 0).detach().cpu().numpy() * 255).astype(np.uint8)

    scores_w = output[0]['scores'].detach().cpu().numpy()
    high_scores_idxs_w = np.where(scores_w > 0.9)[0].tolist()  # Indexes of boxes with scores > 0.9
    post_nms_idxs_w = torchvision.ops.nms(output[0]['boxes'][high_scores_idxs_w], output[0]['scores'][high_scores_idxs_w],
                                        0.3).cpu().numpy()  # Indexes of boxes left after applying NMS (iou_threshold=0.3)]

    keypoints_w = []
    for kps in output[0]['keypoints'][high_scores_idxs_w][post_nms_idxs_w].detach().cpu().numpy():
        keypoints_w.append([list(map(int, kp[:2])) for kp in kps])
    bboxes_w = []
    for bbox in output[0]['boxes'][high_scores_idxs_w][post_nms_idxs_w].detach().cpu().numpy():
        bboxes_w.append(list(map(int, bbox.tolist())))

    #save_image(KEYPOINTS_FOLDER_TEST,1,image_w, bboxes_w, keypoints_w )
        
    print( "Birds detected in image at")
    
    keypoints_w = [[157 , 776] , [538 , 465]]
    print(keypoints_w)

        #^^^^^^^^^^^^# RECONGIZING USING ML #^^^^^^^^^^^^#

        #-----------------------------# WHEN BIRDS ARE DETECTED #------------------------------------------------------#

    #if not(keypoints_w == []) and (len(keypoints_w) ==2):
    if (True):  
       
        W_object = keypoints_w[0]
        B_object = keypoints_w[1]
        #B_object = [157 , 776]
        #W_object = [538 , 465]


        #vvvvvvvvvvvv# INTERSECTION #vvvvvvvvvvvvv#

        bird_coord = find_intersection(image_height_px, image_width_px, v_angle_of_view, down_angle,beam_cam, wall_cam , W_object , B_object) 
        print("Bird detected in 3d space at location")
        print(bird_coord)
        #^^^^^^^^^^^^# INTERSECTION #^^^^^^^^^^^^#

        #vvvvvvvvvvvv# USE LASER #vvvvvvvvvvvvv#
        az, theta = find_az_and_theta(laser_posn , bird_coord)
        print("Turning laser to angles")
        print(az)
        print(theta)
        print("_________________________________________________")
        #^^^^^^^^^^^^# USE LASER #^^^^^^^^^^^^#

        #-----------------------------# WHEN BIRDS ARE DETECTED #------------------------------------------------------#

#-----------------------------#MAIN  LOOP#----------------------------------------------------------------------------------------------#