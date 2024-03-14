import math

def find_az_and_theta(laser_posn , target_posn):
    

    dx = ( target_posn[0]-   laser_posn[0] )
    dy = ( target_posn[1]-   laser_posn[1] )
    dz = ( target_posn[2]-   laser_posn[2] )

    print("dx is " + str(dx))    
    print("dy is " + str(dy))
    print("dz is " + str(dz))


    if (dx ==0):
        dx = 0.00000001

    if (dy ==0):
        dy = 0.00000001

    if (dz ==0):
        dz = 0.00000001

    ground_distance = math.sqrt( (dx * dx) + ( dy * dy ) )

    if (dx > 0):
        if (dy>0):
            az = math.degrees( math.atan( (dy/dx) ) )
        else:
            az = 360+ math.degrees( math.atan( (dy/dx) ) )
    else:
            az = 180 +  math.degrees(  math.atan( (dy/dx) ) )
    
    theta  = math.degrees(math.atan((  abs(dz) /  ground_distance )))

    print(az)
    print(theta)
    return az,theta

#laser_acc = [ 0,0,3 ]
#target_acc = [ -3,-3,3 ]

#find_az_and_theta(laser_acc , target_acc)

#print(  math.degrees(math.atan( -2 )  ))