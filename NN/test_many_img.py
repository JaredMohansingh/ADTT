import torch, os, json, cv2, numpy as np, matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.transforms import functional as F
import albumentations as A
import transforms, utils, engine, train
from utils import collate_fn
from engine import train_one_epoch, evaluate
from datasetclass import ClassDataset, PredDataset
from augmentations import train_transform
from training import get_model
from visualize import visualize
from save_image import save_image



counter = 0
missed = 0

avg_beak_x_error  = 0
avg_beak_y_error  = 0
avg_tail_x_error  = 0
avg_tail_y_error  = 0

beak_error_x = 0
beak_error_y = 0
tail_error_x = 0
tail_error_y = 0


device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'pth_files/low_res_birds_500.pth')
model.to(device)

KEYPOINTS_FOLDER_TEST = 'making_a_dataset/evaluation'
dataset_test = ClassDataset(KEYPOINTS_FOLDER_TEST, transform=None, demo=False)
data_loader_test = DataLoader(dataset_test, batch_size=1, shuffle=False, collate_fn=collate_fn)

iterator = iter(data_loader_test)

for idx in range(len(next(os.walk( KEYPOINTS_FOLDER_TEST +"/Images" ))[2])):
    
    images, targets = next(iterator)
    batch = images
    images = list(image.to(device) for image in images)

    with torch.no_grad():
        model.to(device)
        model.eval()
        output = model(images)

    image = (images[0].permute(1, 2, 0).detach().cpu().numpy() * 255).astype(np.uint8)
    scores = output[0]['scores'].detach().cpu().numpy()

    high_scores_idxs = np.where(scores > 0.7)[0].tolist()  # Indexes of boxes with scores > 0.7
    post_nms_idxs = torchvision.ops.nms(output[0]['boxes'][high_scores_idxs], output[0]['scores'][high_scores_idxs],
                                        0.3).cpu().numpy()  # Indexes of boxes left after applying NMS (iou_threshold=0.3)

    ################################################################################################################
    keypoints_g_truth = []
    for kps in targets[0]['keypoints'].detach().cpu().numpy().astype(np.int32).tolist():
        keypoints_g_truth.append([kp[:2] for kp in kps])
        break

    keypoints = []
    for kps in output[0]['keypoints'][high_scores_idxs][post_nms_idxs].detach().cpu().numpy():
        keypoints.append([list(map(int, kp[:2])) for kp in kps])
        break

    bboxes = []
    for bbox in output[0]['boxes'][high_scores_idxs][post_nms_idxs].detach().cpu().numpy():
        bboxes.append(list(map(int, bbox.tolist())))

    ################################################################################################################
    save_image('making_a_dataset/evaluation/Check', idx  , image, bboxes, keypoints)
    #visualize(idx  , image, bboxes, keypoints)
    f = open('making_a_dataset/evaluation/Annotations/Image'+str(counter)+'.json')
    data = json.load(f)

    if not (keypoints == []):
        beak_error_x =beak_error_x + abs((keypoints_g_truth[0][0][0])-(keypoints[0][0][0]))
        beak_error_y =beak_error_y + abs((keypoints_g_truth[0][0][1])-(keypoints[0][0][1]))
        tail_error_x =tail_error_x + abs((keypoints_g_truth[0][1][0])-(keypoints[0][1][0]))
        tail_error_y =tail_error_y + abs((keypoints_g_truth[0][1][1])-(keypoints[0][1][1]))
    else :
        missed = missed +1 



    counter = counter +1 

avg_beak_x_error =beak_error_x /counter
avg_beak_y_error =beak_error_y /counter
avg_tail_x_error =tail_error_x /counter
avg_tail_y_error =tail_error_y /counter

print("No. of missed detections - "+str(missed))
print("Avg. beak x error in pixels- "+str(avg_beak_x_error))
print("Avg. beak y  error in pixels- "+str(avg_beak_y_error))
print("Avg. tail x  error in pixels- "+str(avg_tail_x_error))
print("Avg. tail y error in pixels- "+str(avg_tail_y_error))

    ################################################################################################################
    #\
    #save_image('making_a_dataset/evaluation', idx  , image, bboxes, keypoints)



#################################################################
