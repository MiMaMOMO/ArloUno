import copy
import cv2
from settings import *
import particle
import camera
import numpy as np
import sys
import commands
import auxiliary


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
    onRobot = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    onRobot = False

def get_cam():
    '''
    Initialize the right camera. 
    '''
    if isRunningOnArlo():
        return camera.Camera(0, 'arlo', useCaptureThread=True)
    else:
        return camera.Camera(0, 'macbookpro', useCaptureThread=True)


### MAIN PROGRAM ###
try:

    # Open windows
    auxiliary.open_windows()

    # Initialize Arlo
    arlo = robot.Robot()

    print("Opening and initializing camera")

    # Check which camera we want to use
    cam = get_cam()

    # Try to selflocalize and get to the center point using the particle filter
    while 1:

        # print("x: {}".format(est_pose.getX()))
        # print("y: {}".format(est_pose.getY()))
        # print("t: {}".format(est_pose.getTheta()))

        # Get a pressed key if any for 10 ms. Maybe if removed could boost performance?
        action = cv2.waitKey(10)

        # Quit if we press q
        if action == ord('q'):
            break
        
        # Fetch next frame
        frame = cam.get_next_frame()

        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(frame)

        if action == ord('f'):
            commands.drive(arlo, dists[0], 0.3)

        # We detected atleast one landmark
        if not isinstance(objectIDs, type(None)):

            # List detected objects
            for i in range(len(objectIDs)):
                print(
                    "Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])

            # Draw detected objects
            cam.draw_aruco_objects(frame)

# Make sure to clean up even if an exception occurred
finally:
    auxiliary.clean_up(cam)
