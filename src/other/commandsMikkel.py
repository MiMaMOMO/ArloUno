import robot
import time

import numpy as np 

from Ex4.Timer import Timer
from settings_alt import *


# Initialize the robot 
arlo = robot.Robot()


def drive(dist, landmark_range = 0.0):
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
            return timer.elapsed_time()
        distance = arlo.read_front_ping_sensor()
        #if distance to a target is 30 cm then stop to avoid collision    
        if distance < 300: 
            arlo.stop()
            return timer.elapsed_time() #how much time did we drive before having to stop

        