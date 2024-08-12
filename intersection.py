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
def find_intersection(image_height =1280, image_width=720 , v_angle_of_view_d =49, beam_cam_posn=[0,0,0], wall_cam_posn = [0,0,0], W_ob_px=[0,0], B_ob_px=[0,0]):


    ## Converting all these to radians
    v_angle_of_view_c = (math.pi /180)*v_angle_of_view_d

    v_focal_length_px = (image_height/2)/(math.tan(v_angle_of_view_c/2))
    ##Vertical and horizontal focal length in pixels should be the same

    down_angle_c = -55 *(math.pi /180)

    wall_x_p = W_ob_px[0]
    wall_y_p = W_ob_px[1]
    beam_x_p = B_ob_px[0]
    beam_y_p = B_ob_px[1]

    ################################################################################################################################################################################
    #generate camera point vector from wall
    ## xfc => extensions from centre

    if (wall_x_p > (image_width/2)):
        wall_xfc_x = wall_x_p -(image_width/2)  
    else:
        wall_xfc_x = -((image_width/2) - wall_x_p) 

    if (wall_y_p > (image_height/2)):
        wall_xfc_y = -(wall_y_p -(image_height/2))  
    else:
        wall_xfc_y = (image_height/2) - wall_y_p 

    ##All this does , is convert the pixel value to a coordinate system where the centre of the image is 0,0
    
    i_wall = 1
    j_wall = wall_xfc_x/v_focal_length_px
    k_wall = wall_xfc_y/v_focal_length_px
    
    ##Augment to fit onto facing xyz plane, ebcause when the vector is generated fro mteh image, there is an error in transforming the x plane to the y plane 
    j_wall = -j_wall

    #If the camera was at 0,0,0 with angle 0,0,0 . this vector would represent the direction of the bird from the camera
    
    #Adjust for rotation about y  axis
    wall_point_posn_vec_i = (i_wall * math.cos(wall_cam_posn[4]*(math.pi /180))) - (k_wall * math.sin(wall_cam_posn[4]*(math.pi /180)))
    wall_point_posn_vec_j = j_wall
    wall_point_posn_vec_k = (i_wall * math.sin(wall_cam_posn[4]*(math.pi /180))) + (k_wall * math.cos(wall_cam_posn[4]*(math.pi /180))) 

    #AND THEN Adjust for rotation about z  axis
    wall_point_posn_vec_i = (wall_point_posn_vec_i * math.cos(wall_cam_posn[5]*(math.pi /180))) - (wall_point_posn_vec_j * math.sin(wall_cam_posn[5]*(math.pi /180)))
    wall_point_posn_vec_j = (wall_point_posn_vec_i * math.sin(wall_cam_posn[5]*(math.pi /180))) + (wall_point_posn_vec_j * math.cos(wall_cam_posn[5]*(math.pi /180)))
    wall_point_posn_vec_k = wall_point_posn_vec_k


    ################################################################################################################################################################################
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
    k_beam = beam_xfc_y/v_focal_length_px

    #If the camera was at 0,0,0 with angle 0,0,0 . this vector would represent the direction of the bird from the camera

    ##Augment to fit onto facing xyz plane, ebcause when the vector is generated fro mteh image, there is an error in transforming the x plane to the y plane 
    j_beam = -j_beam

    #Adjust for rotation about y  axis
    beam_point_posn_vec_i = (i_beam * math.cos(beam_cam_posn[4]*(math.pi /180))) - (k_beam * math.sin(beam_cam_posn[4]*(math.pi /180)))
    beam_point_posn_vec_j = j_beam
    beam_point_posn_vec_k = (i_beam * math.sin(beam_cam_posn[4]*(math.pi /180))) + (k_beam * math.cos(beam_cam_posn[4]*(math.pi /180))) 

    #AND THEN Adjust for rotation about z  axis
    beam_point_posn_vec_i = (beam_point_posn_vec_i * math.cos(beam_cam_posn[5]*(math.pi /180))) - (beam_point_posn_vec_j * math.sin(beam_cam_posn[5]*(math.pi /180)))
    beam_point_posn_vec_j = (beam_point_posn_vec_i * math.sin(beam_cam_posn[5]*(math.pi /180))) + (beam_point_posn_vec_j * math.cos(beam_cam_posn[5]*(math.pi /180)))
    beam_point_posn_vec_k = beam_point_posn_vec_k

    
    ################################################################################################################################################################################

    #Beam
    line_1 = [[beam_cam_posn[0] , beam_cam_posn[1] , beam_cam_posn[2]],[ beam_point_posn_vec_i  , beam_point_posn_vec_j, beam_point_posn_vec_k]]
    # Wall
    line_2 = [[ wall_cam_posn[0] , wall_cam_posn[1] , wall_cam_posn[2]],[ wall_point_posn_vec_i  , wall_point_posn_vec_j, wall_point_posn_vec_k]]


    line_1_input = 0
    line_2_input = 0
    current_line_1 = find_coord(line_1,line_1_input)
    current_line_2 = find_coord(line_2,line_2_input)
    
    turn_on = True
    inter_line_distance = find_distance( current_line_1 , current_line_2)

    distance_tracker = [0,0]
    step = 0.01
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


    #Not in order cause there was a mistake earleir where xyz was changed to xzy , so this line jsut changes it back to xyz

    #print(f" Interpolation result is ->{avg_point}")
    return avg_point
    

###############################################################

d__angle_of_view = 55.0 
h_angle_of_view = 25.73 
v_angle_of_view = 49 


image_width_px = 720 
image_height_px = 1280 

beam_cam_posn= [-2.2 ,0 ,3.0, 0, -55.0 , 0 ]
# wall cam is facing forward , toward positive x values 
# rotation angles are (rotation about the x axis, rotation about the y axis, and rotation about the z axis
#rotation about the x axis is roll (which is not expected to be used)
# roation about y axis is tilt (down angle)
#rotation about z axis is pan (rotation on the xy plane)

wall_cam_posn = [ 2.2, 0, 3.0 , 0 ,-55.0, 180]
#beam cam is facing backwards , towards negative x values 


# TODO - update this to include euler angles of camera . 


W_object = [136, 667] 
B_object = [553, 378]



#bird_coord =  find_intersection(image_height_px, image_width_px, v_angle_of_view, beam_cam_posn, wall_cam_posn , W_object , B_object) 
#print(bird_coord)
#answer = [0.45	, -0.5	, 0.4]
#bird_coord = [-0.5,-0.5,0.93]
#error = find_distance(answer, bird_coord)
#print(f"Error is ->{error}")

