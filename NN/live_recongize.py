import torch,  cv2, numpy as np
from torch.utils.data import  DataLoader
import torchvision
import time
from utils import collate_fn
from datasetclass import  PredDataset
from training import get_model
from save_image import save_image

############# NN SETUP##############
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'ADTT/NN/keypointsrcnn_weights_35.pth')
model.to(device)

KEYPOINTS_FOLDER_TEST = 'ADTT/NN/live_recongize'
############# NN SETUP##############pi


############# CAMERA SETUP##############\


capw = cv2.VideoCapture( 0  +cv2.CAP_DSHOW ) 
capw.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capw.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
capw.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))


capb = cv2.VideoCapture( 1  +cv2.CAP_DSHOW )  
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



#ret, framew = capw.read()
#ret, frameb = capb.read()
count= 1
while True:

    ret, framew = capw.read()
    ret, frameb = capb.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    concat = cv2.vconcat([frameb, framew]) 
    concat = cv2.rotate(concat, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("ADTT/NN/live_recongize/Images/live.jpg", concat) 

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

    #TODO , make lines above run faster somehow
        #t1 = time.time()   - 3.2 seconds

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


    #If one image does not detect a bird, then no detection overall.

    # Below, in output[0]['keypoints'][high_scores_idxs][post_nms_idxs] and output[0]['boxes'][high_scores_idxs][post_nms_idxs]
    # Firstly, we choose only those objects, which have score above predefined threshold. This is done with choosing elements with [high_scores_idxs] indexes
    # Secondly, we choose only those objects, which are left after NMS is applied. This is done with choosing elements with [post_nms_idxs] indexes


    #Uncomment the previous line to show the predicted coordinates in console
    #visualize(1,image, bboxes, keypoints )

    #Note that the function below is for when ONE iMage is in thE prediction foilder
    # and the param 'count' is used to label files , nothing more

    #################### RECONGIZING USING ML##########################

    #save_image(KEYPOINTS_FOLDER_TEST,1,image_w, bboxes_w, keypoints_w )
    #print(keypoints_w)

    if (keypoints_w):
        print("Bird found")
        print(keypoints_w)
        save_image(KEYPOINTS_FOLDER_TEST,count,image_w, bboxes_w, keypoints_w )
        count = count +1
    else:
        print("No bird")

    show_live = cv2.imread('ADTT/NN/live_recongize/Images/live.jpg',1)

    cv2.imshow("image",show_live)

    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
capb.release()
cv2.destroyAllWindows()