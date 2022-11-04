import numpy as np 

from settings import * 
from custom_timer import Timer
from auxiliary import delete_duplicates

# TODO: Remove this 
import time 


def rotate(arlo, angle) -> None:
    '''
    Make Arlo rotate in the right direction and angle. 
    
    Parameters:
        arlo(obj)       : The Arlo robot object.
        angle(float)    : The angle of the robot to a point.
    '''
    
    sign = np.sign(angle)                               # Get the sign of the angle 
    scaled_angle = np.abs(np.degrees(angle))            # Get absolute degrees from radians
    rot_time = scaled_angle * (TIME_ORIENTATION / 90)   # Seconds to to rotate Arlo angle amount 
    
    # Find the direction we should rotate 
    left_dir = 1 if sign == -1 else 0
    right_dir = 1 if sign == 1 else 0
    
    # TODO: Try to initialize the timer after giving the go command to arlo
    # TODO: Use the custom sleep function 
    
    # Make Arlo rotate in the right direction 
    arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, left_dir, right_dir) 
    t = Timer()                                     # Timer to measure a countdown for the rotation
    #t.custom_sleep(0.01)   
    # time.sleep(0.01)
    
    # Control what happens while Arlo rotates or what should happen after a rotation 
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

    scaled_dist = dist / 100                        # Scale the distance down to meters  
    tolerance_time = landmark_range * TIME_METER    # How close we want Arlo to get to the landmark 
    drive_time = scaled_dist * TIME_METER           # How long it takes Arlo to drive dist (cm)

    # TODO: Try to initialize the timer after giving the go command to arlo  
    
    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    t = Timer()                                 # Timer used to measure a countdown for Arlo
    # t.custom_sleep(0.01)
    # time.sleep(0.01)
    
    # Control what happens while Arlo drives and what can happen after 
    while 1:
        
        # TODO: Test this. 
        # Arlo is close enough to the landmark 
        # if arlo.read_front_ping_sensor() <= 400.0:
        #     arlo.stop()
        #     break
        
        # TODO: Check for obstacles here 

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # otherwise let Arlo drive the full dist
        if t.elapsed_time() > (drive_time - tolerance_time):
            arlo.stop()
            break
        
        
def scan(arlo, cam, landmark = None):
    '''
    Scan for Aruco landmarks by rotating x amount of degrees. 
    Scan will search for the landmark given if any. 
    
    Parameters:
        arlo(obj)       : The Arlo robot. 
        cam(obj)        : The camera used. 
        landmark(int)   : The landmark ID we are searching for. 
    '''
    
    # TODO: Find out how long it takes to do a full turn 
    # Rotate a full turn until we find some Aruco landmarks 
    for _ in range(FULL_ROTATION):
        rotate(arlo, DEGREES_20)
        #Timer.custom_sleep(0.6)
        time.sleep(0.6)
        detected = detect(cam)
        
        print("ID:      {}".format(detected[0]))
        print("Dists:   {}".format(detected[1]))
        print("Agnles:  {}".format(detected[2]))
        
        # If we saw an ID 
        if not isinstance(detected[0], type(None)):
            
            # If the ID we saw was the landmark we were searching for 
            if landmark in detected[0]:
                return detected
    
    # TODO: If Arlo does not detect anything, move Arlo to a new position and try again 


def scan_enviroment(arlo, cam):
    '''
    Will scan the entire enviroment to search for all four landmarks, 
    and return their distances and angles and ids. 
    
    Parameters:
        arlo(obj)       : The Arlo object.
        cam(obj)        : The camera used. 
    '''
    
    # Temporary storing arrays for the first scans 
    objectIDs, dists, angles = []
    
    # Begin the scan for all landmakrs starting at 1 
    for i in range(len(LANDMARK_IDS)):
            found_landmark = scan(arlo, cam, RUTE[i])

            # Arlo found the landmark it was scanning for 
            if not isinstance(found_landmark[0], type(None)):
                objectIDs.append(found_landmark[0])
                dists.append(found_landmark[1])
                angles.append(found_landmark[2])
                
    # Check for duplicates and remove them if any was found 
    if not isinstance(objectIDs, type(None)):        
        objectIDs, dists, angles = delete_duplicates(objectIDs, dists, angles)

    # Cast the temporary lists into numpy arrays
    objectIDs = np.array(objectIDs)
    dists = np.array(dists)
    angles = np.array(angles)
    
    return objectIDs, dists, angles


def detect(cam) -> tuple: 
    '''
    Take a frame and try to detect if any landmarks exist in the frame. 
    
    Parameters:
        cam(obj)        : The camera object. 
        frame(img)      : The image we are looking at.
    '''
    
    # Get an image 
    frame = cam.get_next_frame()
    
    # Draw the Aruco detection on the image  
    # cam.draw_aruco_objects(frame)
    
    # Get information from the image 
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    
    # Return the found values. Will be None if no landmarks was detected 
    return objectIDs, dists, angles, frame
