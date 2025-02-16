import math

def find_az_and_theta( laser_posn , target_posn,  clockwise_az = False,  downplus= True):
    #This function only works if the zero position (0 , 0) of the laser is pointing parallel to the x axis facing positive values .

    #clockwise paramenter used to determine which azimuth angle direction laser will turn
    #downplus used to determine if laser going downwards in theta angle corresponds to increasing angle value, if false, down menas decreasing angle value

    #TODO actually incorporate the clockwise thing into this function

    dx = ( target_posn[0]- laser_posn[0] )
    dy = ( target_posn[1]- laser_posn[1] )
    dz = ( target_posn[2]- laser_posn[2] )

    ground_distance = math.sqrt( (dx * dx) + ( dy * dy ) )

    if( dx>0):
        if (dy>0):
            az = math.degrees( math.atan( (dy/dx) ) )
        elif (dy<0):
            az = 360+ math.degrees( math.atan( (dy/dx) ) )
        elif (dy ==0):
            az = 0

    elif (dx <0):
        if (dy ==0):
            az = 180
        else :
            az = 180 +  math.degrees(  math.atan( (dy/dx) ) )

    elif (dx ==0):
        if (dy >0):
            az = 90
        elif (dy <0):
            az= 270
        if (dy ==0):
            az = 0

    if (dz==0):
        theta = 0    
    elif (ground_distance == 0):
        theta = 90
    else:
        theta  = math.degrees(math.atan((  abs(dz) / ground_distance )))

    #print(az)
    #print(theta)
    return az,theta

#laser_acc = [ -1.5, 0.05 ,2 ]
#target_acc = [ -2.5 , 2.5 ,1  ]

#print(find_az_and_theta(laser_acc , target_acc))
