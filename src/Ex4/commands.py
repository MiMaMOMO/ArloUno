import robot
import time

from settings import * 

import numpy as np 
from Timer import Timer


def rotate(arlo, angle) -> None:
    '''
    Make Arlo rotate in the right direction and angle. 
    
    Parameters:
        arlo(obj):      The Arlo robot object 
        angle(float):   The angle of the robot to a point 
    '''
    
    sign = np.sign(angle)                           # Get the sign of the angle 
    scaled_angle = np.abs(np.degrees(angle))        # Make radians into degrees. Get absolute value
    rot_time = scaled_angle * (ORIENTATION / 90)    # Seconds it takes Arlo to rotate angle amount 
    timer = Timer()                                 # Timer to measure a countdown for the rotation
    
    # TODO: Try to initialize the timer after giving the go command to arlo
    
    # Find the direction we should rotate 
    left_dir = 1 if sign == 1 else 0
    right_dir = 1 if sign == -1 else 0
    
    # TODO: Test what happens if we multiply with the sign and get -1. Will it count as a 0? 
    
    # Make Arlo rotate in the right direction 
    arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, left_dir, right_dir) 
    timer.sleep(0.01)
    
    while 1: 
        #print("Real time    : {}".format(time.perf_counter()))
        #print("Elapsed time : {}".format(timer.elapsed_time()))

        # Break when Arlo have spent the seconds needed to perform the rotation 
        if timer.elapsed_time() > rot_time:
            arlo.stop()
            break

def drive(arlo, dist, landmark_range = 0.0) -> None:
    '''
    Make Arlo drive a certain amount of distance. 
    
    Parameters:
        arlo(obj):              The Arlo robot object 
        dist(float):            The distance that Arlo intends on driving in cm.
        landmark_range(float):  How close we want to drive towards a landmark in m 
    '''

    scaled_dist = dist / 100                    # Scale the distance down to meters  
    drive_time = scaled_dist * METER            # How long in seconds it takes Arlo to drive dist
    timer = Timer()                             # Timer used to measure a countdown for Arlo

    # TODO: Try to initialize the timer after giving the go command to arlo  

    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    timer.sleep(0.01)
    
    # Control what happens while Arlo drives with the program 
    # If the amount of time have passed, stop Arlo 
    while 1:
        #print("Real time    : {}".format(time.perf_counter()))
        #print("Elapsed time : {}".format(timer.elapsed_time()))

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # Otherwise let Arlo drive the full dist
        if timer.elapsed_time() > (drive_time - (METER * landmark_range)):
            arlo.stop()
            break    
        
def scan(arlo) -> None:
    '''
    Scan for Aruco landmarks by rotating tiny amounts.
    '''
    pass
