import sys
import cv2

sys.path.append("../rally/")

from settings import *
from camera import Camera
from auxiliary import open_windows, clean_up


# Try to import robot module
try:
    import robot
    ON_ROBOT = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    ON_ROBOT = False


def get_cam():
    '''
    Initialize the right camera. 
    '''

    return Camera(0, 'arlo', useCaptureThread=True)


### MAIN PROGRAM ###
try:

    # Open windows
    open_windows()

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
    clean_up(cam)
