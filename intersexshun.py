import torch, os, json, cv2, numpy as np, matplotlib.pyplot as plt
import os, json, cv2, numpy as np, matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.transforms import functional as F
import albumentations as A
import transforms, utils, engine, train
from utils import collate_fn
from engine import train_one_epoch, evaluate
import math

def find_distance(  p1 , p2):
    x_0 = p1[0]
    y_0 = p1[1]
    z_0 = p1[2]
    x_1 = p2[0]
    y_1 = p2[1]
    z_1 = p2[2]
    return math.sqrt(((x_0-x_1)*(x_0-x_1))+((y_0-y_1)*(y_0-y_1))+((z_0-z_1)*(z_0-z_1)))

def find_coord(line , t):
    x = (line[0][0])+((t)*(line[1][0])) 
    y = (line[0][1])+((t)*(line[1][1]))
    z = (line[0][2])+((t)*(line[1][2]))
    answer_array = [x,y,z]
    return answer_array

def check_for_decrease( variable_line , input, constant_line_point, delta, current_dist ):
    new_dist = find_distance( find_coord(variable_line, input+ delta), constant_line_point)

    if ( new_dist < current_dist ):
        return True
    else:
        return False 


d__angle_of_view = 50.0 
h_angle_of_view = 25.73 
v_angle_of_view = 44.2 
down_angle = -45.0 
## Converting all these to radians
d__angle_of_view = (math.pi /180)*50.0 
h_angle_of_view = (math.pi /180)*25.73 
v_angle_of_view = (math.pi /180)*44.2 
down_angle = (math.pi /180)*(-45.0) 

image_width = 720 
image_height = 1280 

beam_cam = [-2.2 ,0 ,3.0]
# wall cam is facing forward , toward positive x values 

wall_cam = [ 2.1, 0, 3.0]
#beam cam is facing backwards , towards negative x values 

B_y = [331 , 239]
B_r = [594 , 402]
B_g = [486 , 270]

W_r = [160 , 209]
W_g = [234 , 270]
W_y = [396 , 355]

wall_x_p = W_r[0]
wall_y_p = W_r[1]
beam_x_p = B_r[0]
beam_y_p = B_r[1]

##Answers
#world_red = [ -0.327 , 1.588 , -0.343]
#world_green = [-0.047 , 1.667 , -0.193]
#world_yellow = [0.117 , 1.623 , 0.052]
world_target = [ -0.327 , 1.588 , -0.343]

h_focal_length_px = (image_width/2)/(math.tan(h_angle_of_view/2))
v_focal_length_px = (image_height/2)/(math.tan(v_angle_of_view/2))

# Above two values are supposed to be equal , any discrepancy is caused by
# error in initial values (angle of view)

##########################################################################################################################################
#generate camera point vector from wall
## extensions from centre

if (wall_x_p > (image_width/2)):
    wall_xfc_x = wall_x_p -(image_width/2)  
else:
    wall_xfc_x = -((image_width/2) - wall_x_p) 


if (wall_y_p > (image_height/2)):
    wall_xfc_y = -(wall_y_p -(image_height/2))  
else:
    wall_xfc_y = (image_height/2) - wall_y_p 

i_wall = 1
j_wall = wall_xfc_x/h_focal_length_px
k_wall = (wall_xfc_y/(v_focal_length_px))

#Adjust for pointing down
wall_point_posn_vec_i = (i_wall * math.cos(down_angle)) - (k_wall * math.sin(down_angle))
wall_point_posn_vec_j = j_wall
wall_point_posn_vec_k = (i_wall * math.sin(down_angle)) + (k_wall * math.cos(down_angle))  

wall_point_posn_vec_i = -wall_point_posn_vec_i
# ^^ Negate i since it is facing the wrong x direction

# Use position and angle of camera to get camera point vector for position vector
# thing

wall_posn_vec_i = wall_point_posn_vec_i  +wall_cam[0]
wall_posn_vec_j = wall_point_posn_vec_j  +wall_cam[1]
wall_posn_vec_k = wall_point_posn_vec_k  +wall_cam[2]
## NOTE - There are two instances where the k vector needs to be negated but it 
# cancels out so is omitted
#####################################################################################
if (beam_x_p > (image_width/2)):
    beam_xfc_x = beam_x_p -(image_width/2)  
else:
    beam_xfc_x = -((image_width/2) - beam_x_p) 


if (beam_y_p > (image_height/2)):
    beam_xfc_y = -(beam_y_p -(image_height/2))  
else:
    beam_xfc_y = ((image_height/2) - beam_y_p) 

i_beam = 1 
j_beam = beam_xfc_x/h_focal_length_px
k_beam = beam_xfc_y/(v_focal_length_px)

beam_point_posn_vec_i = (i_beam * math.cos(down_angle)) - (k_beam * math.sin(down_angle))
beam_point_posn_vec_j = -j_beam
beam_point_posn_vec_k = (i_beam * math.sin(down_angle)) + (k_beam * math.cos(down_angle))  


beam_posn_vec_i = beam_point_posn_vec_i  +beam_cam[0]
beam_posn_vec_j = beam_point_posn_vec_j  +beam_cam[1]
beam_posn_vec_k = beam_point_posn_vec_k  +beam_cam[2]

##########################################################################################################################################
##########################################################################################################################################

#Beam
line_1 = [[beam_cam[0] , beam_cam[2] , beam_cam[1]],[ beam_point_posn_vec_i  , beam_point_posn_vec_k, beam_point_posn_vec_j]]
# Wall
line_2 = [[ wall_cam[0] , wall_cam[2] , wall_cam[1]],[ wall_point_posn_vec_i  , wall_point_posn_vec_k, wall_point_posn_vec_j]]

line_1_input = 0
line_2_input = 0
current_line_1 = find_coord(line_1,line_1_input)
current_line_2 = find_coord(line_2,line_2_input)
turn_on = True
inter_line_distance = find_distance( current_line_1 , current_line_2)

distance_tracker = [0,0]
step = 0.1
while (turn_on):
#  If this loop runs slow it is because the step is too small    
##########################################################################################################################################

    if (check_for_decrease (line_1, line_1_input , current_line_2, step, inter_line_distance  )):
        line_1_input = line_1_input+ step
        current_line_1 = find_coord(line_1 , line_1_input)

    if (check_for_decrease (line_1, line_1_input , current_line_2, -step, inter_line_distance  )):
        line_1_input= line_1_input -step    
        current_line_1 = find_coord(line_1 , line_1_input)
   
############################################################
    if (check_for_decrease (line_2, line_2_input , current_line_1, step, inter_line_distance  )):
        line_2_input = line_2_input+ step
        current_line_2 = find_coord(line_2 , line_2_input)

    if (check_for_decrease (line_2, line_2_input , current_line_1, -step, inter_line_distance  )):
        line_2_input = line_2_input- step
        current_line_2 = find_coord(line_2 , line_2_input)

##########################################################################################################################################
    inter_line_distance = find_distance( current_line_1 , current_line_2)    
    distance_tracker.pop(0)
    distance_tracker.append(inter_line_distance)

    if ( distance_tracker[0] == inter_line_distance):
        if (distance_tracker[1] == inter_line_distance):
            turn_on = False


avg_point = [1,1,1]
avg_point[0] = ((current_line_1[0])+(current_line_2[0]))/2
avg_point[1] = ((current_line_1[1])+(current_line_2[1]))/2
avg_point[2] = ((current_line_1[2])+(current_line_2[2]))/2

print(f" Interpolation result is ->{avg_point}")
print(f" Predetermined answer is ->{world_target}")
print('The error in distance is ->')
print(find_distance(avg_point , world_target))