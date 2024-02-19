import math

def find_az_and_theta(laser_posn , target_posn):
    laser_posn

    target_posn
    az = math.degrees(math.atan((target_posn[2])/(target_posn[0])))

    theta = math.degrees(math.atan( (( math.sqrt( pow((laser_posn[0])-(target_posn[0]),2) + pow((laser_posn[2])-(target_posn[2]),2) ) ))/(( abs((laser_posn[1])-(target_posn[1])) ))  ))

    return az,theta
