import commands
import cv2
import auxiliary
import sys
import particle

import numpy as np

from selflocalize import compute_weight, resample, copy_resampling_references

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
    

# def run_brute() -> None:
#     '''
#     Run the brute program where we assume no obstacles. 
#     '''
    
#     try:
#         # Open windows
#         auxiliary.open_windows()

#         # Initialize particles
#         particles = particle.initialize_particles(NUM_OF_PARTICLES)

#         # The first estimate of the robots current pose
#         est_pose = particle.estimate_pose(particles)

#         # Initialize Arlo
#         arlo = robot.Robot()

#         # Allocate space for world map
#         world = np.zeros((500, 500, 3), dtype = np.uint8)

#         # Draw map
#         auxiliary.draw_world(est_pose, particles, world)

#         # Check which camera we want to use
#         cam = auxiliary.get_cam()

#         # Which known landmark Arlo will search for 
#         rute_idx = 0
        
#         while 1: 
            
#             # We are back at landmark 1 stop the program 
#             if rute_idx >= 5:
#                 break
            
#             # TODO: Remove this since we wont be pressing any keys to the rally 
#             # Get a pressed key if any for 10 ms
#             action = cv2.waitKey(10)
            
#             # TODO: Remove this since we wont be pressing any keys to the rally
#             # Quit if we press q 
#             if action == ord('q'): 
#                 break
        
#             # Try and detect the first landmark upon starting 
#             objectIDs, dists, angles, frame = commands.detect(cam)
            
#             # Check and remove duplicates 
#             if not isinstance(objectIDs, type(None)):
#                 objectIDs, dists, angles = auxiliary.delete_duplicates(objectIDs, dists, angles)
            
#             # We detected atleast one landmark
#             if not isinstance(objectIDs, type(None)):
                
#                 # The total sum of all weigths
#                 weight_sum = 0.0

#                 # Reset the weights
#                 [p.setWeight(0.0) for p in particles]
                
#                 # List detected objects
#                 for i in range(len(objectIDs)):
#                     print(i)
#                     print(
#                         "Object ID = ", objectIDs[i],
#                         ", Distance = ", dists[i], 
#                         ", angle = ", angles[i]    
#                     )
                        
#                     # Compute the unnormalized weight for each particle in the i'th objectID
#                     for p in particles:

#                         # Weights of particles
#                         weight = compute_weight(objectIDs, i, p, dists, angles)

#                         # Set the particles new weight alongside its former weights
#                         p.setWeight(p.getWeight() + weight)

#                         # Add to the sum of weights
#                         weight_sum += weight
                    
#                     # Rotating and driving towards the found landmark within a certain range
#                     while 1:

#                         # Try and detect the landmark Arlo are focusing on
#                         objectIDs, dists, angles, frame = commands.detect(cam)
                        
#                         # Check and remove duplicates 
#                         if not isinstance(objectIDs, type(None)):
#                             objectIDs, dists, angles = auxiliary.delete_duplicates(
#                                 objectIDs, dists, angles)

#                         # We cannot see anything and we assume we are close to the landmark 
#                         if isinstance(objectIDs, type(None)):
#                             rute_idx += 1
#                             break

#                         # Rotate towards the landmark if the angle is bigger than 13 degrees
#                         if np.abs(angles[i]) > DEGREES_13:
#                             print("Starting rotation with angle = {}".format(angles[i]))
#                             commands.rotate(arlo, angles[i])

#                         # Find the minimum betwen the distance and 1m
#                         dist = np.minimum(dists[i], ONE_METER)
                        
#                         print(dist)
#                         print(dists[i])

#                         # Drive within 40cm of the landmark if the dist < 1m,
#                         # otherwise drive the full length
#                         if dist < ONE_METER:
#                             print("Starting landmark drive with dist = {}".format(dist))
#                             commands.drive(arlo, dist, LANDMARK_RANGE)
#                             rute_idx += 1
#                             break
#                         else:
#                             print("Starting normal drive with dist = {}".format(dist))
#                             commands.drive(arlo, dist)

#                     # Scan
#                     c = commands.scan(arlo, cam, RUTE[rute_idx])

#                     # objectIDs, dists, angles, frame = commands.scan(arlo, cam, 2)
#                     objectIDs = c[0]
#                     dists = c[1]
#                     angles = c[2]
#                     frame = c[3]
                    
#                     if not isinstance(objectIDs, type(None)):
#                         objectIDs, dists, angles = auxiliary.delete_duplicates(
#                             objectIDs, dists, angles)
                
#                 # Store normalized weights of each particle for probability purposes
#                 weights = [(p.getWeight() / weight_sum) for p in particles]

#                 # Resample the particles
#                 resampling = resample(particles, weights)

#                 # Copy the new references of resampling
#                 copy_resampling_references(resampling)

#                 # Replace our particles with the resampling particles
#                 particles = resampling

#                 # Add uncertainity to each particle
#                 particle.add_uncertainty(particles, 1.0, 0.01)

#                 # Draw detected objects
#                 cam.draw_aruco_objects(frame)
#             else:
#                 # No observation - reset weights to uniform distribution
#                 for p in particles:
#                     p.setWeight(1.0 / NUM_OF_PARTICLES)
                    
#             # The estimate of the robots current pose
#             est_pose = particle.estimate_pose(particles) 
                    
#             # Update the windows
#             auxiliary.update_windows(est_pose, particles, world, frame)

#     # Make sure to clean up even if an exception occurred
#     finally: 
#         auxiliary.clean_up(cam)


# ### STARTING POINT OF THE PROGRAM ### 
# if __name__ == '__main__':
#     run_brute()

# # 1. Compute a strategy for blockades 
# # 2. Compute a strategy for obstacles 
# # 3. Make selflocalize into a function which returns Arlos pose 

import commands
import cv2
import auxiliary
import sys
import particle

import numpy as np

from selflocalize import compute_weight, resample, copy_resampling_references

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

        # Try and detect the first landmark upon starting
        objectIDs, dists, angles, frame = commands.detect(cam)
        print(objectIDs)
        print(dists)
        print(angles)

        if not isinstance(objectIDs, type(None)):
            objectIDs, dists, angles = auxiliary.delete_duplicates(
                objectIDs, dists, angles)

        print(objectIDs)
        print(dists)
        print(angles)

        while 1:

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

                # The total sum of all weigths
                # weight_sum = 0.0

                # # TODO: Maybe dont reset to 0, but to uniform distribution instead
                # # TODO: Maybe do this in another loop
                # # Reset the weights
                # [p.setWeight(0.0) for p in particles]

                # List detected objects
                for i in range(len(objectIDs)):
                    print(i)
                    print(
                        "Object ID = ",
                        objectIDs[i],
                        ", Distance = ",
                        dists[i],
                        ", angle = ",
                        angles[i]
                    )

                    # # Compute the unnormalized weight for each particle in the i'th objectID
                    # for p in particles:

                    #     # Weights of particles
                    #     weight = compute_weight(objectIDs, i, p, dists, angles)

                    #     # Set the particles new weight alongside its former weights
                    #     p.setWeight(p.getWeight() + weight)

                    #     # Add to the sum of weights
                    #     weight_sum += weight

                # Rotating and driving towards the found landmark within a certain range
                while 1:

                    # Try and detect the landmark Arlo are focusing on
                    objectIDs, dists, angles, frame = commands.detect(cam)
                    if not isinstance(objectIDs, type(None)):
                        objectIDs, dists, angles = auxiliary.delete_duplicates(
                            objectIDs, dists, angles)

                    # Break if we cannot see anything
                    if isinstance(angles, type(None)):
                        rute_idx += 1
                        break

                    # Rotate towards the landmark if the angle is bigger than 13 degrees
                    if np.abs(angles[i]) > 0.156892:
                        print("Starting rotation.")
                        commands.rotate(arlo, angles[i])

                    # Find the minimum betwen the distance and 1m
                    dist = np.minimum(dists[i], ONE_METER)

                    print(dists[i])
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
                c = commands.scan(arlo, cam, RUTE[rute_idx])

                # objectIDs, dists, angles, frame = commands.scan(arlo, cam, 2)
                objectIDs = c[0]
                dists = c[1]
                angles = c[2]
                frame = c[3]

                if not isinstance(objectIDs, type(None)):
                    objectIDs, dists, angles = auxiliary.delete_duplicates(
                        objectIDs, dists, angles)

                print(objectIDs)
                print(dists)
                print(angles)

                # TODO: Move all particles here otherwise move them after resampling
                # Move all particles according to what we actually drove
                # particle.move_all_particles(particles, dists[i], angles[i])

                # TODO: Use numpy to normalize the weights?
                # Store normalized weights of each particle for probability purposes
                # weights = [(p.getWeight() / weight_sum) for p in particles]

                # # Resample the particles
                # resampling = resample(particles, weights)

                # # TODO: Try copying the reference another way
                # # Copy the new references of resampling
                # copy_resampling_references(resampling)

                # # Replace our particles with the resampling particles
                # particles = resampling

                # # Add uncertainity to each particle
                # particle.add_uncertainty(particles, 1.0, 0.01)

                # Draw detected objects
                cam.draw_aruco_objects(frame)

                # TODO: Find out how we can do a full turn
                # Scan for the next landmark
                # c = commands.scan(arlo, cam, RUTE[rute_idx])

                # # objectIDs, dists, angles, frame = commands.scan(arlo, cam, 2)
                # objectIDs = c[0]
                # dists = c[1]
                # angles = c[2]
                # frame = c[3]
            # else:
            #     # No observation - reset weights to uniform distribution
            #     for p in particles:
            #         p.setWeight(1.0 / NUM_OF_PARTICLES)

            # The estimate of the robots current pose
            #est_pose = particle.estimate_pose(particles)

            # Update the windows
            auxiliary.update_windows(est_pose, particles, world, frame)

    # Make sure to clean up even if an exception occurred
    finally:
        auxiliary.clean_up(cam)


### STARTING POINT OF THE PROGRAM ###
if __name__ == '__main__':
    run()
