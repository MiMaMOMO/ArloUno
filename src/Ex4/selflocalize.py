import copy
import math
import cv2
import particle
import camera
import numpy as np
import sys


# Flags
showGUI = True  # Whether or not to open GUI windows
onRobot = False # Whether or not we are running on the Arlo robot

def isRunningOnArlo():
    """Return True if we are running on Arlo, otherwise False.
      You can use this flag to switch the code from running on you laptop to Arlo - you need to do the programming here!
    """
    return onRobot

if isRunningOnArlo():
    sys.path.append("../")

# Try to import robot module 
try:
    import robot 
    onRobot = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    onRobot = False

# Some color constants in BGR format
CRED = (0, 0, 255)
CGREEN = (0, 255, 0)
CBLUE = (255, 0, 0)
CCYAN = (255, 255, 0)
CYELLOW = (0, 255, 255)
CMAGENTA = (255, 0, 255)
CWHITE = (255, 255, 255)
CBLACK = (0, 0, 0)

# Colors used when drawing the landmarks
landmark_colors = [CRED, CGREEN] 

# The robot knows the position of 2 landmarks. Their coordinates are in the unit centimeters [cm].
landmarkIDs = [3, 4]
landmarks = {
    3: (0.0, 0.0),          # Coordinates for landmark 1 (RED)
    4: (100.0, 0.0)         # Coordinates for landmark 2 (GREEN)
}


def jet(x):
    """Colour map for drawing particles. This function determines the colour of 
    a particle from its weight."""
    r = (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (4.0 * x - 3.0 / 2.0) + (x >= 5.0 / 8.0 and x < 7.0 / 8.0) + (x >= 7.0 / 8.0) * (-4.0 * x + 9.0 / 2.0)
    g = (x >= 1.0 / 8.0 and x < 3.0 / 8.0) * (4.0 * x - 1.0 / 2.0) + (x >= 3.0 / 8.0 and x < 5.0 / 8.0) + (x >= 5.0 / 8.0 and x < 7.0 / 8.0) * (-4.0 * x + 7.0 / 2.0)
    b = (x < 1.0 / 8.0) * (4.0 * x + 1.0 / 2.0) + (x >= 1.0 / 8.0 and x < 3.0 / 8.0) + (x >= 3.0 / 8.0 and x < 5.0 / 8.0) * (-4.0 * x + 5.0 / 2.0)

    return (255.0 * r, 255.0 * g, 255.0 * b)

def draw_world(est_pose, particles, world):
    """Visualization.
    This functions draws robots position in the world coordinate system."""

    # Fix the origin of the coordinate system
    offsetX = 100
    offsetY = 250

    # Constant needed for transforming from world coordinates to screen coordinates (flip the y-axis)
    ymax = world.shape[0]

    world[:] = CWHITE # Clear background to white

    # Find largest weight
    max_weight = 0
    for particle in particles:
        max_weight = max(max_weight, particle.getWeight())

    # Draw particles
    for particle in particles:
        x = int(particle.getX() + offsetX)
        y = ymax - (int(particle.getY() + offsetY))
        colour = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x,y), 2, colour, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX, 
                                     ymax - (int(particle.getY() + 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x,y), b, colour, 2)

    # Draw landmarks
    for i in range(len(landmarkIDs)):
        ID = landmarkIDs[i]
        lm = (int(landmarks[ID][0] + offsetX), int(ymax - (landmarks[ID][1] + offsetY)))
        cv2.circle(world, lm, 5, landmark_colors[i], 2)

    # Draw estimated robot pose
    a = (int(est_pose.getX())+offsetX, ymax-(int(est_pose.getY())+offsetY))
    b = (int(est_pose.getX() + 15.0*np.cos(est_pose.getTheta()))+offsetX, 
                                 ymax-(int(est_pose.getY() + 15.0*np.sin(est_pose.getTheta()))+offsetY))
    cv2.circle(world, a, 5, CMAGENTA, 2)
    cv2.line(world, a, b, CMAGENTA, 2)

def initialize_particles(num_particles):
    particles = np.empty(num_particles, dtype = type(particle.Particle))
    
    # Random starting points for each particle 
    for i in range(num_particles):
        p = particle.Particle(
            600.0 * np.random.ranf() - 100.0, 
            600.0 * np.random.ranf() - 250.0, 
            np.mod(2.0 * np.pi * np.random.ranf(), 2.0 * np.pi), 
            1.0 / num_particles
        )
        
        particles[i] = p

    return particles


### MAIN PROGRAM ###
try:
    
    # Open windows 
    if showGUI:
        WIN_RF1 = "Robot view"
        cv2.namedWindow(WIN_RF1)
        cv2.moveWindow(WIN_RF1, 50, 50)

        WIN_World = "World view"
        cv2.namedWindow(WIN_World)
        cv2.moveWindow(WIN_World, 500, 50)

    # Initialize particles
    num_particles = 100
    particles = initialize_particles(num_particles)

    # The estimate of the robots current pose
    est_pose = particle.estimate_pose(particles) 

    # Driving parameters
    velocity = 0.0              # cm/sec
    angular_velocity = 0.0      # radians/sec
    
    # Spread 
    spread_dist = 30.0          # The spread for the distance 
    spread_angle = 1.0          # The spread for the orientation 

    # TODO: Initialize the robot (XXX: You do this). We can only initialize when using Arlo 
    # arlo = robot.Robot()

    # Allocate space for world map
    world = np.zeros((500, 500, 3), dtype = np.uint8)

    # Draw map
    draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    if isRunningOnArlo():
        cam = camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        cam = camera.Camera(0, 'macbookpro', useCaptureThread = True)
        
    while 1:

        # Move the robot according to user input (only for testing)
        action = cv2.waitKey(10)
        if action == ord('q'): # Quit
            break
    
        if not isRunningOnArlo():
            if action == ord('w'): # Forward
                velocity += 4.0
            elif action == ord('x'): # Backwards
                velocity -= 4.0
            elif action == ord('s'): # Stop
                velocity = 0.0
                angular_velocity = 0.0
            elif action == ord('a'): # Left
                angular_velocity += 0.2
            elif action == ord('d'): # Right
                angular_velocity -= 0.2
        
        # TODO: Use motor controls to update particles
        # XXX: Make the robot drive 

        # Fetch next frame
        colour = cam.get_next_frame()
        
        # Detect objects
        objectIDs, dists, angles = cam.detect_aruco_objects(colour)
        
        # We detected atleast one landmark 
        if not isinstance(objectIDs, type(None)):
            
            # List detected objects
            for i in range(len(objectIDs)):
                print("Object ID = ", objectIDs[i], ", Distance = ", dists[i], ", angle = ", angles[i])
                # TODO: Do something for each detected object - remember, the same ID may appear several times if we look angular at one box. If that happens maybe pick the ArUco landmark with the closest mark 

            # Compute particle weights
            weight_sum = 0.0                        # The total sum of all weigths 
            
            # Compute the unnormalized weight for each particle 
            for p in particles:
                
                # Compute weights for each particle by using their distance 
                x = landmarks[objectIDs[0]][0] - p.getX()
                y = landmarks[objectIDs[0]][1] - p.getY()
                
                dist = np.sqrt(pow(x, 2) + pow(y, 2))
                dist_weight = np.exp(-(pow(dists[0] - dist, 2) / (2 * pow(spread_dist, 2))))
                
                # Compute weights for each particle by using their orientation
                orientation_vector = np.array([np.cos(p.getTheta()), np.sin(p.getTheta())])
                orthogonal_vector = np.array([-orientation_vector[1], orientation_vector[0]])
                pointing_vector = np.array([x, y]) / dist
                
                orientation_sign = np.sign(np.dot(pointing_vector, orthogonal_vector))
                inverse_cos = np.arccos(np.dot(pointing_vector, orientation_vector))
                angle_landmark = orientation_sign * inverse_cos
                orientation = angles[0] - angle_landmark
                orientation_weight = np.exp(-(pow(orientation, 2) / (2 * pow(spread_angle, 2))))
                
                # Set the particles new weight 
                p.setWeight(dist_weight * orientation_weight)
                
                # Add to the sum of weights
                weight_sum += p.getWeight()
            
            # Store normalized weights of each particle for probability purposes 
            weights = [(p.getWeight() / weight_sum) for p in particles]
            
            # Resample the particles 
            resampling = np.random.choice(
                a = particles, 
                size = num_particles, 
                replace = True, 
                p = weights
            )
            
            # Copy the new references of resampling
            for i in range(len(resampling)): 
                resampling[i] = copy.deepcopy(resampling[i])
                
            # Replace our particles with the resampling particles 
            particles = resampling
            
            # Add uncertainity to each particle 
            particle.add_uncertainty(particles, 1.0, 0.05)
            
            # Draw detected objects
            cam.draw_aruco_objects(colour)
        else:
            # No observation - reset weights to uniform distribution
            for p in particles:
                p.setWeight(1.0 / num_particles)

        # The estimate of the robots current pose
        est_pose = particle.estimate_pose(particles) 

        # Update the world map 
        if showGUI:
            draw_world(est_pose, particles, world)      # Draw map
            cv2.imshow(WIN_RF1, colour)                 # Show frame
            cv2.imshow(WIN_World, world)                # Show world
  
# Make sure to clean up even if an exception occurred
finally: 
    cv2.destroyAllWindows()         # Close all windows
    cam.terminateCaptureThread()    # Clean-up capture thread
