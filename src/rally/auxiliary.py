import cv2
import camera

import numpy as np

from settings import *


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
            
            # Find shortest distance between the two duplicates 
            if dists[duplicate_indexes[0][0]] < dists[duplicate_indexes[0][1]]: 
                idx_to_delete = duplicate_indexes[0][1]
            else: 
                idx_to_delete = duplicate_indexes[0][0]
            
            # Delete the further distance values found 
            objectIDs = np.delete(objectIDs, idx_to_delete)
            dists = np.delete(dists, idx_to_delete)
            angles = np.delete(angles, idx_to_delete)

    return objectIDs, dists, angles


def remove_unknown(objectIDs, dists, angles) -> tuple:
    '''
    Takes 3 correlated lists of IDs, dists and angles and then removes unknown IDs and
    their correspondning dists and angles based on the list landmarks(known landmarks).
    
    Parameters: 
        objectIDs(array)        : Found landmarks.
        dists(array)            : Aruco distances. 
        angles(array)           : Aruco landmarks angles. 
        landmarks(array)        : The landmarks we know on the map. 
    '''
    
    known_objectIDs = np.array([id for id in objectIDs if id in LANDMARKS])
    known_dists = np.array([dist for dist, id in zip(dists, objectIDs) if id in LANDMARKS])
    known_angles = np.array([angle for angle, id in zip(angles, objectIDs) if id in LANDMARKS])
    
    if not isinstance(known_objectIDs, type(None)):
        return known_objectIDs, known_dists, known_angles
    else:
        return objectIDs, dists, angles
    
    # if len(objectIDs) == 0:
    #     objectIDs = None
    #     return known_objectIDs, known_dists, known_angles
    # else:
    #     return objectIDs, dists, angles


def remove_known(objectIDs, dists, angles, landmarks) -> tuple:
    '''
    Takes 3 correlated lists of IDs, dists and angles and then removes known IDs and
    their correspondning dists and angles based on the list landmarks(known landmarks). 
    
    Parameters: 
        objectIDs(array)        : Found landmarks.
        dists(array)            : Aruco distances. 
        angles(array)           : Aruco landmarks angles. 
        landmarks(array)        : The landmarks we know on the map.
    '''
    
    if objectIDs is not None:
        known_dists = [dist for dist, id in zip(
            dists, objectIDs) if id not in landmarks]
        known_angles = [angle for angle, id in zip(
            angles, objectIDs) if id not in landmarks]
        known_objectIDs = [id for id in objectIDs if id not in landmarks]
        if len(objectIDs) == 0:
            objectIDs = None
        return known_objectIDs, known_dists, known_angles
    else:
        return objectIDs, dists, angles
