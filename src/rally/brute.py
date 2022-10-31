import commands
import cv2

from brute_settings import * 
from selflocalize import * 


# Open windows
open_windows()

# Initialize particles
particles = initialize_particles(num_particles)

# The first estimate of the robots current pose
est_pose = particle.estimate_pose(particles)

# Initialize Arlo
arlo = robot.Robot()

# Allocate space for world map
world = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw map
draw_world(est_pose, particles, world)

# Check which camera we want to use
cam = get_cam()

# Visted landmarks 
visited = []

# Start value for IDS, distances and angles 
objectIDs, dists, angles = None 

def run() -> None: 
    '''
    Run brute program.
    '''
    
    try:
        while 1: 
            
            # Get a pressed key if any for 10 ms. Maybe if removed could boost performance?
            action = cv2.waitKey(10)
            
            # Quit if we press q 
            if action == ord('q'): 
                break
            
            if action == ord('f'):
                objectIDs, dists, angles = commands.detect(arlo, cam)
            
            # We detected atleast one landmark
            if not isinstance(objectIDs, type(None)):
                
                # The total sum of all weigths
                weight_sum = 0.0

                # Reset the weights
                [p.setWeight(0) for p in particles]
                
                # List detected objects
                for i in range(len(objectIDs)):
                    print(
                        "Object ID = ", 
                        objectIDs[i], 
                        ", Distance = ", 
                        dists[i], 
                        ", angle = ", 
                        angles[i]    
                    )

                    # Compute the unnormalized weight for each particle in the i'th objectID
                    for p in particles:

                        # Weights of particles
                        weight = compute_weight(objectIDs, i, p, dists, angles)

                        # Set the particles new weight alongside its former weights
                        p.setWeight(p.getWeight() + weight)

                        # Add to the sum of weights
                        weight_sum += weight
                        
                    # Rotate and drive towards the seen landmark 
                    commands.rotate(arlo, angles[i])
                    commands.drive(arlo, dists[i], 0.3)
                    
                    # We visited the ith landmark 
                    visited.append(objectIDs[i])
                
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
                
                # Scan for the next landmark 
                objectIDs, dists, angles = commands.scan(arlo, visited[-1] + 1)
            else:
                # No observation - reset weights to uniform distribution
                for p in particles:
                    p.setWeight(1.0 / num_particles)
                    
            # Update the windows
            update_windows(est_pose, particles, world, frame)

    # Make sure to clean up even if an exception occurred
    finally: 
        clean_up(cam)
