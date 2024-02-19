import torch,  cv2, numpy as np
from torch.utils.data import  DataLoader
import torchvision
from NN.utils import collate_fn
from NN.datasetclass import  PredDataset
from NN.training import get_model
from NN.save_image import save_image
from intersection import find_intersection
from laser_aimer import find_az_and_theta

###############################INITIALIZE##################################################################################

    ############# INTERSECTION ##############    

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

B_object = [157 , 776]
W_object = [538 , 465]
#default values

    ############# INTERSECTION ##############

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
    ############# CAMERA SETUP##############

    ############# NN SETUP##############
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'ADTT/NN/pth_files/low_res_birds_80.pth')
model.to(device)

KEYPOINTS_FOLDER_TEST = 'ADTT/NN/live_recongize'
    ############# NN SETUP##############    

###############################INITIALIZE##################################################################################

###############################MAIN  LOOP#######################################
while (True):

        #######################TAKE PCITURES#############################

    ret, framew = capw.read()
    ret, frameb = capb.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    concat = cv2.hconcat([framew, frameb]) 
    cv2.imwrite("ADTT/NN/live_recongize/Images/live.jpeg", concat) 
        #######################TAKE PCITURES#############################
    
        #################### RECONGIZING USING ML##########################
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
        #################### RECONGIZING USING ML##########################

    print(keypoints_w)
    if not(keypoints_w == []):
        W_object = keypoints_w[0]
        B_object = keypoints_w[1]
        
        #######################INTERSEXSHUN#####################################
        bird_coord = find_intersection(image_height_px, image_width_px, v_angle_of_view, down_angle,beam_cam, wall_cam , W_object , B_object) 
        #######################INTERSEXSHUN#####################################

        ###########################USE LASER#######################################
        az, theta = find_az_and_theta(laser_posn , bird_coord)
        ###########################USE LASER#######################################

###############################MAIN  LOOP#######################################