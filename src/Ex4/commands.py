import robot
import time

import numpy as np 

# from Ex4.Timer import Timer
# from Ex4.settings import *

from settings import * 
from Timer import Timer


# Initialize the robot 
# arlo = robot.Robot()


def rotate(arlo, angle) -> None:
    '''
    Make Arlo rotate in the right direction and angle. 
    '''
    
    sign = np.sign(angle)
    scaled_angel = np.abs(np.degrees(angle))                # Make radians into degrees 
    rot_time = scaled_angel * (ORIENTATION / 90)   # Seconds it takes Arlo to rotate angle amount 
    timer = Timer()                                 # Timer used to measure a countdown for Arlo
    
    # Find the direction we should rotate 
    left_dir = 0
    right_dir = 0
    
    print(sign)
    
    if sign == -1.0:
        right_dir = 1
        print(right_dir)
    else:
        left_dir = 1
        print(left_dir)
    
    # Make Arlo rotate in the right direction 
    arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, right_dir, left_dir) 
    time.sleep(0.01)
    
    while 1: 
        
        # If Arlo wants to go near a box we account for that by a certain tolerance
        # Otherwise let Arlo drive the full dist
        if timer.elapsed_time() > rot_time:
            arlo.stop()
            break
    

def drive(arlo, dist, landmark_range = 0.0) -> None:
    '''
    Make Arlo drive a certain amount of distance. 
    
    Parameters:
        dist(float):            The distance that Arlo intends on driving in cm.
        landmark_range(float):  How close we want to drive towards a landmark in m 
    '''

    scaled_dist = dist / 100                    # Scale the distance down to meters  
    drive_time = scaled_dist * METER            # How long in seconds it takes Arlo to drive dist
    timer = Timer()                             # Timer used to measure a countdown for Arlo

    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    time.sleep(0.01)
    
    # Control what happens while Arlo drives with the program 
    # If the amound of time have passed, stop Arlo 
    while 1:

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # Otherwise let Arlo drive the full dist
        if timer.elapsed_time() > (drive_time - (METER * landmark_range)):
            arlo.stop()
            break    


# rotate(0.2617)
