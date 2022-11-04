import commands
import cv2
import auxiliary
import sys
import particle

import numpy as np
from settings import *

if ON_ROBOT:
    sys.path.append("../robot")

# Try to import robot module
try:
    import robot
    ON_ROBOT = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    ON_ROBOT = False

# Start value for IDS, distances and angles
# objectIDs = None
# dists = None
# angles = None


def run() -> None:
    '''
    Run a brute program where we assume no obstacles. 
    '''

    try:
        # Open windows
        auxiliary.open_windows()

        # Initialize particles
        particles = particle.initialize_particles(NUM_OF_PARTICLES)

        # The first estimate of the robots current pose
        est_pose = particle.estimate_pose(particles)

        # Initialize Arlo
        arlo = robot.Robot()

        # Allocate space for world map
        world = np.zeros((500, 500, 3), dtype=np.uint8)

        # Draw map
        auxiliary.draw_world(est_pose, particles, world)

        # Check which camera we want to use
        cam = auxiliary.get_cam()

        # Which known landmark Arlo will search for
        rute_idx = 0

        # Get the first frame
        # frame = cam.get_next_frame()

        print(RUTE[rute_idx])

        while 1:
            
            # Try and detect the first landmark upon starting
            objectIDs, dists, angles, frame = commands.scan(arlo, cam, RUTE[rute_idx])
            print(objectIDs)
            print(dists)
            print(angles)

            # We are back at landmark 1 stop the program
            if rute_idx >= 5:
                break

            # TODO: Remove this since we wont be pressing any keys to the rally
            # Get a pressed key if any for 10 ms
            action = cv2.waitKey(10)

            # TODO: Remove this since we wont be pressing any keys to the rally
            # Quit if we press q
            if action == ord('q'):
                break

            # We detected atleast one landmark
            if not isinstance(objectIDs, type(None)):


                print(RUTE[rute_idx])
                print(objectIDs[0])

                # Rotating and driving towards the found landmark within a certain range
                while 1:
                    print("!!!!!")

                    # Try and detect the landmark Arlo are focusing on
                    objectIDs, dists, angles, _ = commands.detect(cam)

                    print(objectIDs)

                    # Break if we cannot see anything
                    if isinstance(objectIDs, type(None)):
                        print("Cannot see.")
                        rute_idx += 1
                        break

                    # Rotate towards the landmark if the angle is bigger than 13 degrees
                    if np.abs(angles[0]) > 0.156892:
                        print("Starting rotation.")
                        commands.rotate(arlo, angles[0])

                    # Find the minimum betwen the distance and 1m
                    dist = np.minimum(dists[0], ONE_METER)

                    print(dists[0])
                    print(dist)

                    # Drive within 30cm of the landmark if the dist < 1m,
                    # otherwise drive the full length
                    if dist < ONE_METER:
                        print("Starting landmark drive.")
                        commands.drive(arlo, dist, LANDMARK_RANGE)
                        rute_idx += 1
                        break
                    else:
                        print("Starting normal drive.")
                        commands.drive(arlo, dist)

                    print(rute_idx)

                # Scan
                objectIDs, dists, angles, frame = commands.scan(arlo, cam, RUTE[rute_idx])
                print(objectIDs)
                print(dists)
                print(angles)

            # Draw detected objects
            cam.draw_aruco_objects(frame)

        # Update the windows
        # auxiliary.update_windows(est_pose, particles, world, frame)

    # Make sure to clean up even if an exception occurred
    finally:
        auxiliary.clean_up(cam)


### STARTING POINT OF THE PROGRAM ###
if __name__ == '__main__':
    run()
