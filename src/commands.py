import robot
import time

from Ex4.Timer import Timer
from Ex4.settings import *


# Initialize the robot 
arlo = robot.Robot()

print("Initialized!")


def rotate(angle, dir) -> None:
    '''
    Make Arlo rotate in the right direction and angle. 
    '''
    
    pass 
    # timer = Timer()                             # Timer used to measure a countdown for Arlo
    
    # # Make Arlo rotate in the right direction 
    # arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, 1, 1) 
    
    # while 1: 
        
    #     # If Arlo wants to go near a box we account for that by a certain tolerance
    #     # Otherwise let Arlo drive the full dist
    #     if timer.elapsed_time() > ()):
    #         arlo.stop()
    #         break
    

def drive(dist, landmark_range = 0.0) -> None:
    '''
    Make Arlo drive a certain amount of distance. 
    
    Parameters:
        dist(float):            The distance that Arlo intends on driving in cm.
        landmark_range(float): How close we want to drive towards a landmark in m 
    '''
    print("Driving!")

    scaled_dist = dist / 100                    # Scale the distance down to meters  
    drive_time = scaled_dist * METER            # How long in seconds it takes Arlo to drive dist
    timer = Timer()                             # Timer used to measure a countdown for Arlo

    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    #time.sleep(0.01)
    
    # Control what happens while Arlo drives with the program 
    # If the amound of time have passed, stop Arlo 
    #while 1:

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # Otherwise let Arlo drive the full dist
    #if timer.elapsed_time() > (drive_time - (METER * landmark_range)):
    if timer.elapsed_time() > 3:
        print("Stop!")
        arlo.stop()
        #break   
        
drive(200)  
print("Drived!")  
