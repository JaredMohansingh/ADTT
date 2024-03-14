import math

def find_distance(  p1 , p2):
    x_0 = p1[0]
    y_0 = p1[1]
    z_0 = p1[2]
    x_1 = p2[0]
    y_1 = p2[1]
    z_1 = p2[2]
    return math.sqrt(((x_0-x_1)*(x_0-x_1))+((y_0-y_1)*(y_0-y_1))+((z_0-z_1)*(z_0-z_1)))

###############################################################
def find_coord(line , t):
    x = (line[0][0])+((t)*(line[1][0])) 
    y = (line[0][1])+((t)*(line[1][1]))
    z = (line[0][2])+((t)*(line[1][2]))
    answer_array = [x,y,z]
    return answer_array
###############################################################
def check_for_decrease( variable_line , input, constant_line_point, delta, current_dist ):
    new_dist = find_distance( find_coord(variable_line, input+ delta), constant_line_point)

    if ( new_dist < current_dist ):
        return True
    else:
        return False 


###############################################################
def find_intersection(image_height =1280, image_width=720 , v_angle_of_view_d =49, 
                      down_angle_d = -55, beam_cam_posn=[0,0,0], wall_cam_posn = [0,0,0], W_ob_px=[0,0], B_ob_px=[0,0]):


    ## Converting all these to radians
    v_angle_of_view_c = (math.pi /180)*v_angle_of_view_d
    down_angle_c = (math.pi /180)*(down_angle_d) 

    v_focal_length_px = (image_height/2)/(math.tan(v_angle_of_view_c/2))
    ##Vertical and horizontal focal length in pixels should be the same

    wall_x_p = W_ob_px[0]
    wall_y_p = W_ob_px[1]
    beam_x_p = B_ob_px[0]
    beam_y_p = B_ob_px[1]

    ########################################################################################
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
    j_wall = wall_xfc_x/v_focal_length_px
    k_wall = (wall_xfc_y/(v_focal_length_px))

    

    #Adjust for pointing down
    wall_point_posn_vec_i = (i_wall * math.cos(down_angle_c)) - (k_wall * math.sin(down_angle_c))
    wall_point_posn_vec_j = j_wall
    wall_point_posn_vec_k = (i_wall * math.sin(down_angle_c)) + (k_wall * math.cos(down_angle_c)) 

    wall_point_posn_vec_i = -wall_point_posn_vec_i
    # ^^ Negate i since it is facing the wrong x direction

    ########################################################################################
    #generate camera point vector from beam
    ## extensions from centre
    if (beam_x_p > (image_width/2)):
        beam_xfc_x = beam_x_p -(image_width/2)  
    else:
        beam_xfc_x = -((image_width/2) - beam_x_p) 


    if (beam_y_p > (image_height/2)):
        beam_xfc_y = -(beam_y_p -(image_height/2))  
    else:
        beam_xfc_y = ((image_height/2) - beam_y_p) 

    i_beam = 1 
    j_beam = beam_xfc_x/v_focal_length_px
    k_beam = beam_xfc_y/(v_focal_length_px)

    beam_point_posn_vec_i = (i_beam * math.cos(down_angle_c)) - (k_beam * math.sin(down_angle_c))
    beam_point_posn_vec_j = -j_beam
    beam_point_posn_vec_k = (i_beam * math.sin(down_angle_c)) + (k_beam * math.cos(down_angle_c))  
    #TODO This should be defined better, using teh cartesian location of the camera and the euler rotation angles.

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
    avg_point[2] = ((current_line_1[1])+(current_line_2[1]))/2
    avg_point[1] = ((current_line_1[2])+(current_line_2[2]))/2


    #Not in order cause there was a mistake earleir where xyz was changed to xzy , so this line jsut changes it back to xyz

    print(f" Interpolation result is ->{avg_point}")
    return avg_point
    ######    x,     z,     y
    #answer = [0.5,  0,   0.5]
    #error = find_distance(answer, avg_point)
    #print(f"Error is ->{error}")

###############################################################

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
# TODO - update this to include euler angles of camera . 


## This is literally jsut to test it
B_object = [177,449]
W_object = [571, 790]

#bird_coord = find_intersection(image_height_px, image_width_px, v_angle_of_view, down_angle,beam_cam, wall_cam , W_object , B_object) 
        