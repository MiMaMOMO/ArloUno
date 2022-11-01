import numpy as np 
import time
import camera 
import sys 

from settings import * 


def isRunningOnArlo():
    """Return True if we are running on Arlo, otherwise False.
      You can use this flag to switch the code from running on you laptop to Arlo - you need to do the programming here!
    """
    return ON_ROBOT

if isRunningOnArlo():
    sys.path.append("../robot")

# Try to import robot module
try:
    import robot
    ON_ROBOT = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    ON_ROBOT = False


# TODO: Remove this and learn to fucking import a class 
class Timer:
    def __init__(self) -> None:
        self.start_time = time.perf_counter()

    def elapsed_time(self) -> float:
        '''
        The elapsed time since we initialized this object. 
        
        Returns:
            The elapsed time between initializen and now. 
        '''
        return (time.perf_counter() - self.start_time)

    def sleep(self, val) -> None:
        '''
        Sleeps a certain amount of time. 
        '''

        # Sleep val time in seconds
        time.sleep(val)



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
    t = Timer()                                     # Timer to measure a countdown for the rotation
    
    # Find the direction we should rotate 
    left_dir = 1 if sign == 1 else 0
    right_dir = 1 if sign == -1 else 0
    
    # TODO: Test what happens if we multiply with the sign and get -1. Will it count as a 0? 
    
    # Make Arlo rotate in the right direction 
    arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, left_dir, right_dir) 
    t.sleep(0.01)
    
    # TODO: Try to initialize the timer after giving the go command to arlo
    
    # Control what happens while Arlo rotates 
    while 1: 

        # Break when Arlo have spent the seconds needed to perform the rotation 
        if t.elapsed_time() > rot_time:
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
    t = Timer()                                 # Timer used to measure a countdown for Arlo

    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    t.sleep(0.01)
    
    # TODO: Try to initialize the timer after giving the go command to arlo  
    
    # Control what happens while Arlo drives
    while 1:

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # otherwise let Arlo drive the full dist
        if t.elapsed_time() > (drive_time - (METER * landmark_range)):
            arlo.stop()
            break    
        
        
def scan(arlo, camera, landmark = None):
    '''
    Scan for Aruco landmarks by rotating tiny amounts.
    '''
    
    # TODO: Numpy this 
    # Rotate a full turn until we find some Aruco landmarks 
    for _ in range(FULL_ROTATION):
        rotate(arlo, DEGREES_10)
        detected = detect(camera)
        
        print(detected)
        
        # If anything was detected return the information 
        if not isinstance(detected[0], type(None)):
            if landmark in detected[0]:
                return detected


def detect(cam) -> tuple: 
    '''
    Take a frame and try to detect if any landmarks exist in the frame. 
    '''
    
    # Start by taking an image
    frame = cam.get_next_frame()
    
    # Get information form the image 
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    
    # Do something with that information 
    return objectIDs, dists, angles, frame


# arlo = robot.Robot()

# rotate(arlo, 3.13)
# drive(arlo, 100.0)
