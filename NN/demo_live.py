import torch,  cv2, numpy as np
from torch.utils.data import  DataLoader
import torchvision
import time
from utils import collate_fn
from datasetclass import  PredDataset
from training import get_model
from save_image import save_image
from visualize import visualize

############# NN SETUP##############
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'NN/pth_files/low_res_birds_500.pth')
model.to(device)

KEYPOINTS_FOLDER_TEST = 'NN/live_recongize'
############# NN SETUP##############


############# CAMERA SETUP##############

count = 0 
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



ret, framew = capw.read()
ret, frameb = capb.read()

while True:

    retw, framew = capw.read()
    retb, frameb = capb.read()


    if not retw:
        print("WWWWWWWWWWWWWWWW  Can't receive frame (stream end?). Exiting ...")
        break
    

    if not retb:
        print("BBBBBBBBBBBBBBBB  Can't receive frame (stream end?). Exiting ...")
        break
    

    concat = cv2.vconcat([frameb, framew]) 
    concat = cv2.rotate(concat, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite("NN/live_recongize/Images/live.jpg", concat) 

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
    #visualize(1,concat, bboxes_w, keypoints_w )

    #Note that the function below is for when ONE iMage is in thE prediction foilder
    # and the param 'count' is used to label files , nothing more

    #save_image(KEYPOINTS_FOLDER_TEST,1,image_w, bboxes_w, keypoints_w )

    #print(keypoints_w)
    show_live = cv2.imread('NN/live_recongize/Images/live.jpg',1)

    if not(keypoints_w == []):
        print( "Birds detected in image at")
        print(keypoints_w)
        save_image(KEYPOINTS_FOLDER_TEST,count,image_w, bboxes_w, keypoints_w )
        count= count +1

    cv2.imshow("image",concat)
    if cv2.waitKey(1) == ord('0'):
        break
# When everything done, release the capture

capw.release()
capb.release()
cv2.destroyAllWindows()