import cv2
import camera

import numpy as np

from settings import *
from commands import rotate, drive, detect


def jet(x) -> tuple:
    '''
    frame map for drawing particles. This function determines the frame of 
    a particle from its weight.
    
    PArameters:
        x(float)    : The weight of the particle divided by the max weight. 
    '''
    
    r = (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (4.0 * x - 3.0 / 2.0) + (x >= 5.0 / 8.0 and x < 7.0 / 8.0) + (x >= 7.0 / 8.0) * (-4.0 * x + 9.0 / 2.0)
    
    g = (x >= 1.0 / 8.0 and x < 3.0 / 8.0) * (4.0 * x - 1.0 / 2.0) + (x >= 3.0 / 8.0 and x < 5.0 / 8.0) + (x >= 5.0 / 8.0 and x < 7.0 / 8.0) * (-4.0 * x + 7.0 / 2.0)
    
    b = (x < 1.0 / 8.0) * (4.0 * x + 1.0 / 2.0) + (x >= 1.0 / 8.0 and x < 3.0 / 8.0) + (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (-4.0 * x + 5.0 / 2.0)

    return (255.0 * r, 255.0 * g, 255.0 * b)


def draw_world(est_pose, particles, world) -> None:
    '''
    Visualization.
    This functions draws robots position in the world coordinate system, 
    alongside the particles and the landmarks. 
    
    Parameters:
        est_pose(Particle)  : Arlos particles.
        particles(list)     : The particles. 
        world(ndarray)      : The digital world. 
    '''

    # Fix the origin of the coordinate system
    offsetX = 25
    offsetY = 125

    # Transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]

    world[:] = CWHITE  # Clear background to white

    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX() + offsetX)
        y = ymax - (int(particle.getY() + offsetY))
        frame = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x, y), 2, frame, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX,
             ymax - (int(particle.getY() + 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x, y), b, frame, 2)

    # Draw landmarks
    for i in range(len(LANDMARK_IDS)):
        ID = LANDMARK_IDS[i]
        lm = (int(LANDMARKS[ID][0] + offsetX),
              int(ymax - (LANDMARKS[ID][1] + offsetY)))
        cv2.circle(world, lm, 5, LANDMARK_COLORS[i], 2)

    # Draw estimated robot pose
    a = (int(est_pose.getX())+offsetX, ymax-(int(est_pose.getY())+offsetY))
    b = (int(est_pose.getX() + 15.0 * np.cos(est_pose.getTheta()))+offsetX,
         ymax-(int(est_pose.getY() + 15.0 * np.sin(est_pose.getTheta()))+offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)


def open_windows() -> None:
    '''
    Opens the two windows of Arlo and the particle world if show gui is on. 
    '''

    # Open Arlos window and the particle worlds window
    if SHOW_GUI:
        cv2.namedWindow(WIN_RF1)
        cv2.moveWindow(WIN_RF1, ARLO_WIN_X, ARLO_WIN_Y)
        cv2.namedWindow(WIN_WORLD)
        cv2.moveWindow(WIN_WORLD, WORLD_WIN_X, WORLD_WIN_Y)


def update_windows(est_pose, particles, world, frame) -> None:
    '''
    Updates the world maps. 
    
    Parameters:
        est_pose(Particle)      : Arlos particle.
        particles(list)         : All the particles.
        world(ndarray)          : The digital world.
        frame(img)              : The image we are looking at.
    '''
    
    # Update the world map
    if SHOW_GUI:
        draw_world(est_pose, particles, world)      # Draw map
        cv2.imshow(WIN_RF1, frame)                  # Update frame
        cv2.imshow(WIN_WORLD, world)                # Update world


def compute_center(fst_landmark_idx, sec_landmark_idx) -> tuple:
    '''
    Compute the center point between two known landmarks.
    '''
    
    # Compute the virtual center points x and y coordinate 
    center_x = (LANDMARKS[fst_landmark_idx][0] + LANDMARKS[sec_landmark_idx][0]) / 2
    center_y = (LANDMARKS[fst_landmark_idx][1] + LANDMARKS[sec_landmark_idx][1]) / 2

    return (center_x, center_y)


def compute_center_parameters(center, arlo_pose) -> tuple:
    '''
    Compute the distance and angle from Arlo to the center point between the landmarks.
    
    Parameters:
        center(tuple)           : The not visual point in the center.
        arlo_pose(Particle)     : The Arlo particle. 
    '''                    
    
    # Compute the distance between the center point and Arlo 
    x = center[0] - arlo_pose.getX()
    y = center[1] - arlo_pose.getY()
    dist = np.sqrt(pow(x, 2) + pow(y, 2))
    
    # Compute the angle between the center point and Arlo and absolute angle  
    angle = (arlo_pose.getTheta() - np.arccos(y / dist)) * 180 / np.pi
    abs_angle = np.abs(angle)
    
    # Compute the sign so we knoew if we should move right or left 
    sign = np.sign(angle)
    
    return dist, abs_angle, sign 


def get_cam() -> object:
    '''
    Get the right camera. 
    '''
    
    # Tell the program which camera we want to use 
    if ON_ROBOT:
        return camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        return camera.Camera(0, 'macbookpro', useCaptureThread = True)


def clean_up(cam) -> None:
    '''
    Clean up after we have self localized.
    
    Parameters:
        cam(obj)        : The camera we initialized.
    '''
    
    # Close all windows and clean-up capture thread 
    cv2.destroyAllWindows()         
    cam.terminateCaptureThread()   


def delete_duplicates(objectIDs, dists, angles) -> tuple:
    '''
    Find and delete the duplicates and choose the right ones depending on 
    the shortest distance.
    
    Parameters:
        objectIDs(array)        : Found landmarks.
        dists(array)            : Aruco distances. 
        angles(array)           : Aruco landmarks angles. 
    '''
    
    # Find the dupplicate items 
    duplicates = [ID for idx, ID in enumerate(objectIDs) if ID in objectIDs[:idx]]

    # Remove the duplicated landmarks at random if any was found 
    if duplicates:
        
        # Traverse the duplicates for comparison 
        for duplicate in duplicates:
            
            # Find all index values having the duplicate 
            duplicate_indexes = np.where(objectIDs == duplicate)
            idx_to_delete = 0
            
            # Find shortest distance between the duplicates 
            if dists[duplicate_indexes[0][0]] < dists[duplicate_indexes[0][1]]: 
                idx_to_delete = duplicate_indexes[0][1]
            else: 
                idx_to_delete = duplicate_indexes[0][0]
            
            # Delete the distance which didnt make it alongside its ID and angle 
            objectIDs = np.delete(objectIDs, idx_to_delete)
            dists = np.delete(dists, idx_to_delete)
            angles = np.delete(angles, idx_to_delete)

    return objectIDs, dists, angles


def remove_ids(objectIDs, dists, angles, ids) -> tuple:
    '''
    Takes 3 correlated lists of IDs, dists and angles and then removes unknown/known IDs and
    their correspondning dists and angles based on the landmarks/obstacles known or unknown.
    
    Parameters: 
        objectIDs(array)        : Found landmarks.
        dists(array)            : Aruco distances. 
        angles(array)           : Aruco landmarks angles. 
        ids(array)              : The landmarks/obstacles. 
    '''
    
    # Keep the landmark objects IDs if they are known 
    dists = np.array([dist for dist, id in zip(dists, objectIDs) if id in ids])
    angles = np.array([angle for angle, id in zip(angles, objectIDs) if id in ids])
    objectIDs = np.array([id for id in objectIDs if id in ids])
    
    # If we removed anything and the list is empty, set it to None 
    if not isinstance(objectIDs, type(None)):
        if len(objectIDs) == 0:
            objectIDs, dists, angles = None, None, None
            
    return objectIDs, dists, angles


def move_to_box(arlo, cam, objectIDs, dists, angles, box_range, ids) -> None:
    '''
    After locking into a target box then Arlo will rotate and move towards,
    the Aruco box until Arlo is close enough. 
    
    Parameters:
        arlo(obj)       : The Arlo robot.
        cam(obj)        : The camera used for the program. 
    '''
    
    # Start the rotations and driving towards the choosen obstacle
    while 1:

        # Arlo cannot see anything and we assume we are close to the obstacle
        if isinstance(objectIDs, type(None)):
            print("Breaking!!!")
            break

        # Rotate towards the obstacle if the angle is bigger than 13 degrees
        if np.abs(angles[0]) > DEGREES_13:
            rotate(arlo, angles[0])

        # Print the distance 
        print("Distance: {}".format(dists[0]))

        # Drive within 60cm of the obstacle if the dist < 1.1m,
        # otherwise drive the full length
        if (dists[0] - ONE_METER) <= 10.0:
            print("Starting final drive.")
            drive(arlo, dists[0], box_range)
            break
        else:
            print("Starting normal drive.")
            drive(arlo, NORMAL_DRIVE)

        # Try and detect the obstacle Arlo are focusing on
        # TODO: What if Arlo sees two boxes here? This can happen with landmarks or if Arlo sees two obstacles at the same time. Maybe implement a filter so Arlo only focuses on the focuses obstacle?
        objectIDs, dists, angles = detect(cam, ids)
    

def filter_out(objectIDs, dists, angles, focused_id) -> tuple: 
    '''
    ...
    '''
    
    # Find the index to delete which are not focused 
    dists = np.array([dist for dist, id in zip(dists, objectIDs) if id in focused_id])
    angles = np.array([angle for angle, id in zip(angles, objectIDs) if id in focused_id])
    objectIDs = np.array([id for id in objectIDs if id in focused_id])

    # If we removed anything and the list is empty, set it to None
    if not isinstance(objectIDs, type(None)):
        if len(objectIDs) == 0:
            objectIDs, dists, angles = None, None, None

    return objectIDs, dists, angles
    
    
    


# def remove_landmarks(objectIDs, dists, angles) -> tuple:
#     '''
#     Takes 3 correlated lists of IDs, dists and angles and then removes known IDs and
#     their correspondning dists and angles based on the list landmarks(known landmarks). 
    
#     Parameters: 
#     ---
#         * objectIDs(array)        : Found landmarks.
#         * dists(array)            : Aruco distances. 
#         * angles(array)           : Aruco landmarks angles. 
#         * `landmarks(array)`       : The landmarks we know on the map.
#     '''
    
#     unknown_objectIDs = np.array([id for id in objectIDs if id not in LANDMARK_IDS])
#     unknown_dists = np.array([dist for dist, id in zip(dists, objectIDs) if id not in LANDMARK_IDS])
#     unknown_angles = np.array([angle for angle, id in zip(angles, objectIDs) if id not in LANDMARK_IDS])

#     if not isinstance(objectIDs, type(None)):
#         if len(unknown_objectIDs) == 0:
#             unknown_objectIDs = None
#             unknown_dists = None
#             unknown_angles = None
            
#     return unknown_objectIDs, unknown_dists, unknown_angles
