import torch, os, json, cv2, numpy as np, matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.transforms import functional as F
import albumentations as A
import transforms, utils, NN.engine as engine, train
from utils import collate_fn
from engine import train_one_epoch, evaluate
from datasetclass import ClassDataset, PredDataset
from augmentations import train_transform
from training import get_model
from visualize import visualize
from save_image import save_image
import time

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

model = get_model(num_keypoints = 2, weights_path = 'pth_files/low_res_birds_500.pth')
model.to(device)


KEYPOINTS_FOLDER_TEST = 'making_a_dataset/try'
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

image = (images[0].permute(1, 2, 0).detach().cpu().numpy() * 255).astype(np.uint8)

scores = output[0]['scores'].detach().cpu().numpy()

high_scores_idxs = np.where(scores > 0.9)[0].tolist()  # Indexes of boxes with scores > 0.7

post_nms_idxs = torchvision.ops.nms(output[0]['boxes'][high_scores_idxs], output[0]['scores'][high_scores_idxs],
                                    0.3).cpu().numpy()  # Indexes of boxes left after applying NMS (iou_threshold=0.3)

# Below, in output[0]['keypoints'][high_scores_idxs][post_nms_idxs] and output[0]['boxes'][high_scores_idxs][post_nms_idxs]
# Firstly, we choose only those objects, which have score above predefined threshold. This is done with choosing elements with [high_scores_idxs] indexes
# Secondly, we choose only those objects, which are left after NMS is applied. This is done with choosing elements with [post_nms_idxs] indexes


keypoints = []
for kps in output[0]['keypoints'][high_scores_idxs][post_nms_idxs].detach().cpu().numpy():
    keypoints.append([list(map(int, kp[:2])) for kp in kps])

bboxes = []
for bbox in output[0]['boxes'][high_scores_idxs][post_nms_idxs].detach().cpu().numpy():
    bboxes.append(list(map(int, bbox.tolist())))


#Uncomment the previous line to show the predicted coordinates in console
#visualize(1,image, bboxes, keypoints )

#Note that the function below is for when ONE iMage is in thE prediction foilder
# and the param 'count' is used to label files , nothing more
save_image("making_a_dataset/try",1,image, bboxes, keypoints )

