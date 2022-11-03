import copy
import cv2
from settings import *
import particle
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
    ON_ROBOT = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    ON_ROBOT = False


def compute_weight(objectIDs, i, p, dists, angles) -> float:
    '''
    Compute the weigth of a particle. 
    
    Parameters: 
        objectIDs(list)     : List of found Aruco landmarks. 
        i(int)              : The index of the objectIDs. 
        p(Particle)         : The current particle. 
        dists(list)         : The distances of the Aruco landmarks.
        angles(list)        : The angles of the Aruco landmarks.
    '''
    
    # Compute weights for each particle by using their distance 
    x = LANDMARKS[objectIDs[i]][0] - p.getX() 
    y = LANDMARKS[objectIDs[i]][1] - p.getY() 
    
    dist = np.sqrt(np.power(x, 2) + np.power(y, 2))
    dist_weight = np.exp(-1 * (np.power(dists[i] - dist, 2) / (2 * np.power(SPREAD_DIST, 2))))

    # Compute weights for each particle by using their orientation
    orientation_vector = np.array([np.cos(p.getTheta()), np.sin(p.getTheta())])
    orthogonal_vector = np.array([-orientation_vector[1], orientation_vector[0]])
    pointing_vector = np.array([x, y]) / dist

    orientation_sign = np.sign(np.dot(pointing_vector, orthogonal_vector))
    inverse_cos = np.arccos(np.dot(pointing_vector, orientation_vector))
    angle_landmark = orientation_sign * inverse_cos
    orientation = angles[i] - angle_landmark 
    orientation_weight = np.exp(-1 * (np.power(orientation, 2) / (2 * np.power(SPREAD_ANGLE, 2))))
    
    return (dist_weight * orientation_weight)


def resample(particles, weights) -> np.ndarray:
    '''
    Resample the particles.
    
    Parameters:
        particles(ndarray)      : Array of particles.
        weights(ndarray)        : Array of computed weights. 
    '''
    
    # Resample the particles using SIR 
    return np.random.choice(particles, NUM_OF_PARTICLES, True, weights)


def copy_resampling_references(resampling) -> None:
    '''
    Copy the references for each particle in the resampling.
    '''
    
    # TODO: Numpy this 
    # Make sure we copy the reference and still resample into a new array
    for i in range(len(resampling)): 
        resampling[i] = copy.deepcopy(resampling[i])


# ### MAIN PROGRAM ###
try:
    
    # Open windows 
    auxiliary.open_windows()

    # Initialize particles
    particles = particle.initialize_particles(NUM_OF_PARTICLES)

    # The estimate of the robots current pose
    est_pose = particle.estimate_pose(particles) 
    
    # Middlepoint between the two landmarks (GOAL)
    # XXX: center_point = compute_center()

    # Initialize Arlo  
    arlo = robot.Robot()

    # Allocate space for world map
    world = np.zeros((500, 500, 3), dtype = np.uint8)

    # Draw map
    auxiliary.draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    
    # Check which camera we want to use 
    cam = auxiliary.get_cam()
    
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
        
        if action == ord('d'):
            arlo_x = est_pose.getX()
            arlo_y = est_pose.getY()
            arlo_theta = est_pose.getTheta()
            
            # Tell Arlo to rotate and drive 
            # commands.rotate(arlo, DEGREES_180)
            # commands.drive(arlo, METER_1)
            
            # Compute the new position of Arlo 
            x, y, theta = particle.new_position(est_pose, DEGREES_180, METER_1)
            
            # Move arlo in the digital world 
            # particle.move_particle(est_pose, x, y, theta)
            
            # Move all particles in the digital world 
            particle.move_all_particles(particles, METER_1, DEGREES_180)
            
            # TODO: Tweak the values of uncertainity. Keep them high compared to normal 
            # Add uncertainty to each particles 
            # particle.add_uncertainty(particles, 5.0, 0.05)
        
        # TODO: Use motor controls to update particles.
        # TODO: Compute a driving strategy for making sure to see both landmarks. 
        # XXX: Make the robot drive 
        # Step 1. Keep turning the robot until it can see both landmarks. 
        # Step 2. If Arlo makes a full turn and have not seen both landmarks, 
        # one of the landmarks is probably behind the other. Make Arlo drive x, 
        # amount of meters to either left or right. 
        # Step 3. Self localize by estimating Arlos position using the 
        # landmarks and the particle filter. 
        # Step 4. Pinpoint the location of the center point, Arlos distance and angle.
        # Step 5. Use the angle to turn towards the center point. 
        # Step 6. Use the distance to move Arlo towards the center point. 
        # Step 7. Remember to update the particles position.
        # Step 8. Check if the distance is within a certain tolerance level
        # of the center point. GOAL. 
        
        
        # Fetch next frame
        frame = cam.get_next_frame()
        
        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(frame)
        
        if action == ord('f'):
            commands.drive(arlo, dists[0], 0.3)
        
        # We detected atleast one landmark 
        if not isinstance(objectIDs, type(None)):
            
            # The total sum of all weigths
            weight_sum = 0.0
            
            # Delete the duplicate if we see the same landmark in one frame 
            # objectIDs, dists, angles = delete_duplicates(objectIDs, dists, angles)
            
            # Reset the weights 
            [p.setWeight(0) for p in particles]

            # List detected objects
            for i in range(len(objectIDs)):
                print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
                
                # Compute the unnormalized weight for each particle in the i'th objectID  
                for p in particles:
                    
                    # Weights of particles 
                    weight = compute_weight(objectIDs, i, p, dists, angles)

                    # Set the particles new weight alongside its former weights 
                    p.setWeight(p.getWeight() + weight)
                
                    # Add to the sum of weights
                    weight_sum += weight
            
            # Store normalized weights of each particle for probability purposes 
            weights = [(p.getWeight() / weight_sum) for p in particles]
            
            # Resample the particles 
            resampling = resample(particles, weights)
            
            # Copy the new references of resampling
            copy_resampling_references(resampling)
                
            # Replace our particles with the resampling particles 
            particles = resampling
            
            # Add uncertainity to each particle 
            particle.add_uncertainty(particles, 1.0, 0.01)
            
            # Draw detected objects
            cam.draw_aruco_objects(frame)
        else:
            # No observation - reset weights to uniform distribution
            for p in particles:
                p.setWeight(1.0 / NUM_OF_PARTICLES)

        # The estimate of the robots current pose
        est_pose = particle.estimate_pose(particles) 

        # Update the windows 
        auxiliary.update_windows(est_pose, particles, world, frame)
  
# Make sure to clean up even if an exception occurred
finally: 
    auxiliary.clean_up(cam)
