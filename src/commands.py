import robot

from Ex4.Timer import Timer
from Ex4.settings import LEFT_VELOCITY, RIGHT_VELOCITY, METER


# Initialize the robot 
arlo = robot.Robot()


def rotate(angle, dir) -> None:
    '''
    Make Arlo rotate in the right direction and angle. 
    '''
    pass

def drive(dist, aruco_tolerance = 0.0) -> None:
    '''
    Make Arlo drive a certain amount of distance. 
    
    Parameters:
        dist(float):            The distance that Arlo intends on driving in cm.
        aruco_tolerance(float): How close we want to drive towards a landmark in cm 
    '''

    scaled_dist = dist / 100                    # Scale the distance down to meters  
    drive_time = scaled_dist * METER            # How long in seconds it takes Arlo to drive dist
    timer = Timer()                             # Timer used to measure a countdown for Arlo

    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    
    # Control what happens while Arlo drives with the program 
    # If the amound of time have passed, stop Arlo 
    while 1:

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # Otherwise let Arlo drive the full dist
        if timer.elapsed_time() > (drive_time - (METER * aruco_tolerance)):
            arlo.stop()
            break       
