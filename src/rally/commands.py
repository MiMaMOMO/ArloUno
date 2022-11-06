import numpy as np 

from settings import * 
from custom_timer import Timer
import auxiliary as aux


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
    t = Timer()                                         # Timer to measure a countdown 
    
    # Find the direction we should rotate 
    left_dir = 1 if sign == -1 else 0
    right_dir = 1 if sign == 1 else 0
    
    # Make Arlo rotate in the right direction 
    arlo.go_diff(LEFT_ROT_VELOCITY, RIGHT_ROT_VELOCITY, left_dir, right_dir)   
    t.custom_sleep(0.01)
    
    # Control what happens while Arlo rotates or what should happen after a rotation 
    while 1: 

        # Break when Arlo have spent the seconds needed to perform the rotation 
        if t.elapsed_time() >= rot_time:
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

    scaled_dist = dist / ONE_METER                  # Scale the distance down to meters  
    drive_time = (scaled_dist * TIME_METER)         # How long it takes Arlo to drive dist (cm)
    landmark_time = landmark_range * TIME_METER     # How long it takes to drive landmark range 
    t = Timer()                                     # Timer used to measure a countdown for Arlo
    
    # Make Arlo drive forward 
    arlo.go_diff(LEFT_VELOCITY, RIGHT_VELOCITY, 1, 1) 
    t.custom_sleep(0.1)
    
    # Control what happens while Arlo drives and what can happen after 
    while 1:
        
        # If we are to close to a landmark stop Arlo 
        if arlo.read_front_ping_sensor() < 350.0: 
            arlo.stop()
            break

        # If Arlo wants to go near a box we account for that by a certain tolerance 
        # otherwise let Arlo drive the full dist
        if t.elapsed_time() >= (drive_time - landmark_time):
            arlo.stop()
            break
        
        
def scan_landmarks(arlo, cam, landmark = None):
    '''
    Scan for Aruco landmarks by rotating x amount of degrees. 
    Scan will search for the landmark given if any. 
    
    Parameters:
        arlo(obj)       : The Arlo robot. 
        cam(obj)        : The camera used. 
        landmark(int)   : The landmark ID we are searching for. 
    '''
    t = Timer()
    
    # Rotate a full turn until we find some Aruco landmarks 
    for i in range(FULL_ROTATION):
        print("Iteration: {}".format(i))
        objectIDs, dists, angles = detect(cam, LANDMARK_IDS)           # Try to detect landmarks
        
        print("ID:      {}".format(objectIDs))
        print("Dists:   {}".format(dists))
        print("Agnles:  {}".format(angles))
        
        # Arlo detected a landmark ID  
        if not isinstance(objectIDs, type(None)):
            
            # The ID we saw was the landmark Arlo was searching for 
            if landmark in objectIDs:
                return objectIDs, dists, angles
        
        # Arlo didnt find what it was looking for. Rotate 20 degrees 
        rotate(arlo, DEGREES_20)
        t.custom_sleep(1.0)
    
    return None, None, None
        
        
def scan_obstacles(arlo, cam):
    '''
    Scan for Aruco landmarks by rotating x amount of degrees. 
    Scan will search for the landmark given if any. 
    
    Parameters:
        arlo(obj)       : The Arlo robot. 
        cam(obj)        : The camera used. 
        landmark(int)   : The landmark ID we are searching for. 
    '''
    t = Timer()
        
    # Rotate a full turn until we find some Aruco landmarks 
    for i in range(FULL_ROTATION):
        print("Iteration: {}".format(i))
        objectIDs, dists, angles = detect(cam, OBSTACLES_IDS)           # Try to detect landmarks
        
        print("ID:      {}".format(objectIDs))
        print("Dists:   {}".format(dists))
        print("Agnles:  {}".format(angles))
        
        # Arlo detected a landmark ID  
        if not isinstance(objectIDs, type(None)):
            
            # Add the found obstacles to the lists 
            # ret_objectIDs.append(objectIDs)
            # ret_dists.append(dists)
            # ret_angles.append(angles)
            
            # The ID we saw was the obstacle Arlo was searching for
            #if obstacle in objectIDs:
            return objectIDs, dists, angles
        
        # Arlo didnt find what it was looking for. Rotate 20 degrees 
        rotate(arlo, DEGREES_20)
        t.custom_sleep(1.0)
        
    return objectIDs, dists, angles
        
        
def detect(cam, ids) -> tuple: 
    '''
    Take a frame and try to detect if any landmarks exist in the frame. 
    
    Parameters:
        cam(obj)        : The camera object. 
        frame(img)      : The image we are looking at.
    '''
    
    # Take several frames and get the latest one
    frame = cam.get_next_frame()
    
    # Get information from the image 
    objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    
    # The camera detected some boxes so try to remove obstacle boxes 
    if not isinstance(objectIDs, type(None)):
        objectIDs, dists, angles = aux.remove_ids(objectIDs, dists, angles, ids)
    
        # Landmarks are still in our detection so try to delte any duplicates 
        if not isinstance(objectIDs, type(None)):
            if len(objectIDs) > 0:
                objectIDs, dists, angles = aux.delete_duplicates(objectIDs, dists, angles)
    
    # Return the found values. Will be None if no landmarks was detected 
    return objectIDs, dists, angles


# def detect(cam) -> tuple: 
#     '''
#     Take a frame and try to detect if any landmarks exist in the frame. 
    
#     Parameters:
#         cam(obj)        : The camera object. 
#     '''
    
#     # Take several frames and get the latest one
#     frame = cam.get_next_frame()
    
#     # Get information from the image 
#     objectIDs, dists, angles = cam.detect_aruco_objects(frame)
    
#     # We found an obstacle. Check and delete duplicates
#     if not isinstance(objectIDs, type(None)):
#         print("Starting removal of known objects.")
#         objectIDs, dists, angles = remove_ids(objectIDs, dists, angles, OBSTACLES_IDS)
    
#         # Obstacles are still in our detection so try to delte any duplicates
#         if not isinstance(objectIDs, type(None)):
#             if len(objectIDs) > 0:
#                 objectIDs, dists, angles = delete_duplicates(objectIDs, dists, angles)
    
#     # Return the found values. Will be None if no landmarks was detected 
#     return objectIDs, dists, angles, frame


# def scan_enviroment(arlo, cam):
#     '''
#     Will scan the entire enviroment to search for all four landmarks, 
#     and return their distances and angles and ids. 
    
#     Parameters:
#         arlo(obj)       : The Arlo object.
#         cam(obj)        : The camera used. 
#     '''
    
#     # Temporary storing arrays for the first scans 
#     objectIDs, dists, angles = []
    
#     # Begin the scan for all landmakrs starting at 1 
#     for i in range(len(LANDMARK_IDS)):
#         found_landmark = scan_landmarks(arlo, cam, RUTE[i])

#         # Arlo found the landmark it was scanning for 
#         if not isinstance(found_landmark[0], type(None)):
#             objectIDs.append(found_landmark[0])
#             dists.append(found_landmark[1])
#             angles.append(found_landmark[2])
                
#     # Check for duplicates and remove them if any was found 
#     if not isinstance(objectIDs, type(None)):        
#         objectIDs, dists, angles = aux.delete_duplicates(objectIDs, dists, angles)

#     # Cast the temporary lists into numpy arrays
#     objectIDs = np.array(objectIDs)
#     dists = np.array(dists)
#     angles = np.array(angles)
    
#     return objectIDs, dists, angles
