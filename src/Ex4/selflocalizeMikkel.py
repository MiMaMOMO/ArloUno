import copy
import cv2
import particle
import camera
import numpy as np
import sys
from time import sleep

from tests.remove_duplicate import remove_unkown
#sys.path.append('../')


# Flags
showGUI = True  # Whether or not to open GUI windows
onRobot = False  # Whether or not we are running on the Arlo robot

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
landmarkIDs = [1, 3]
landmarks = {
    1: (0.0, 0.0),          # Coordinates for landmark 1 (RED)
    3: (300.0, 0.0)         # Coordinates for landmark 2 (GREEN)
}

# General parameters 
num_particles = 1000        # The number of particles 
WIN_RF1 = "Robot view"      # The name of the Arlo window
WIN_World = "World view"    # The name of the particle window 

# Driving parameters
velocity = 0.0              # cm/sec
angular_velocity = 0.0      # radians/sec

# Spread parameters  
spread_dist = 15.0          # The spread for the distance 
spread_angle = 1.0          # The spread for the orientation 


def jet(x):
    """frame map for drawing particles. This function determines the frame of 
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
        frame = jet(particle.getWeight() / max_weight)
        cv2.circle(world, (x,y), 2, frame, 2)
        b = (int(particle.getX() + 15.0*np.cos(particle.getTheta()))+offsetX, 
                                     ymax - (int(particle.getY() + 15.0*np.sin(particle.getTheta()))+offsetY))
        cv2.line(world, (x,y), b, frame, 2)

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
    '''
    Initialize a set of particles in a numpy array. 
    '''
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

def open_windows():
    '''
    Opens the two windows of Arlo and the particle world if show gui is on. 
    '''
    if showGUI:
        # Open Arlos window
        cv2.namedWindow(WIN_RF1)
        cv2.moveWindow(WIN_RF1, 50, 50)
        
        # Open the particle world 
        cv2.namedWindow(WIN_World)
        cv2.moveWindow(WIN_World, 500, 50)

def update_windows(est_pose, particles, world, frame):
    '''
    Updates the world maps. 
    '''
    # Update the world map
    if showGUI:
        draw_world(est_pose, particles, world)      # Draw map
        cv2.imshow(WIN_RF1, frame)                  # Show frame
        cv2.imshow(WIN_World, world)                # Show world

def compute_center():
    '''
    Compute the target of Arlo which is the center between the two landmarks. 
    '''
    center_x = (landmarks[1][0] + landmarks[2][0]) / 2
    center_y = (landmarks[1][1] + landmarks[2][1]) / 2
    
    return (center_x, center_y)

def get_cam():
    '''
    Initialize the right camera. 
    '''
    if isRunningOnArlo():
        return camera.Camera(0, 'arlo', useCaptureThread = True)
    else:
        return camera.Camera(0, 'macbookpro', useCaptureThread = True)

def control_with_input(action, velocity, angular_velocity):
    '''
    Update the particles according to input from the keyboard. 
    ''' 
    if not isRunningOnArlo():
        if action == ord('w'):          # Forward
            velocity += 4.0
        elif action == ord('x'):        # Backwards
            velocity -= 4.0
        elif action == ord('s'):        # Stop
            velocity = 0.0
            angular_velocity = 0.0
        elif action == ord('a'):        # Left
            angular_velocity += 0.2
        elif action == ord('d'):        # Right
            angular_velocity -= 0.2

def compute_weight(objectIDs, i, p, dists, angles):
    '''
    Compute each particles weight. 
    '''
    # Compute weights for each particle by using their distance 
    x = landmarks[objectIDs[i]][0] - p.getX() # XXX 
    y = landmarks[objectIDs[i]][1] - p.getY() # XXX 
    
    dist = np.sqrt(pow(x, 2) + pow(y, 2))
    dist_weight = np.exp(-(pow(dists[i] - dist, 2) / (2 * pow(spread_dist, 2)))) # XXX 

    # Compute weights for each particle by using their orientation
    orientation_vector = np.array([np.cos(p.getTheta()), np.sin(p.getTheta())])
    orthogonal_vector = np.array([-orientation_vector[1], orientation_vector[0]])
    pointing_vector = np.array([x, y]) / dist

    orientation_sign = np.sign(np.dot(pointing_vector, orthogonal_vector))
    inverse_cos = np.arccos(np.dot(pointing_vector, orientation_vector))
    angle_landmark = orientation_sign * inverse_cos
    orientation = angles[i] - angle_landmark # XXX 
    orientation_weight = np.exp(-(pow(orientation, 2) / (2 * pow(spread_angle, 2))))
    
    return (dist_weight * orientation_weight)

def resample(particles, weights):
    '''
    Resample the particles.
    '''
    return np.random.choice(particles, num_particles, True, weights)

def copy_resampling_references(resampling):
    '''
    Copy the references for each particle in the resampling.
    '''
    for i in range(len(resampling)): 
        resampling[i] = copy.deepcopy(resampling[i])

def clean_up(cam):
    '''
    Clean up after we have self localized.
    '''
    cv2.destroyAllWindows()         # Close all windows
    cam.terminateCaptureThread()    # Clean-up capture thread


def delete_duplicates(objectIDs, dists, angles):
    '''
    Find and delete the duplicates and choose the right ones depending on angle. 
    '''
    # TODO: Delete the duplicate which have the wrong angle from Arlo. 
    # Find the dupplicate indexes and reverse the order for deletion 
    duplicate_idx = [idx for idx, item in enumerate(objectIDs) if item in objectIDs[:idx]]
    duplicate_idx_sorted = sorted(duplicate_idx, reverse = True)

    # Remove the duplicated landmarks at random 
    if duplicate_idx_sorted:
        for idx in duplicate_idx_sorted:
            objectIDs = np.delete(objectIDs, idx) 
            dists = np.delete(dists, idx) 
            angles = np.delete(angles, idx) 
            
    return objectIDs, dists, angles
                    
def compute_center_parameters(center, arlo_pose):
    '''
    Compute the distance and angle from Arlo to the center point between the landmarks. 
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

def remove_unknown(objectIDs, dists, angles, landmarks):
    '''
    Takes 3 correlated lists of IDs, dists and angles and then removes unknown IDs and
    their correspondning dists and angles based on the list landmarks(known landmarks).
    '''
    if objectIDs is not None:
        known_dists = [dist for dist, id in zip(dists, objectIDs) if id in landmarks]
        known_angles = [angle for angle, id in zip(angles, objectIDs) if id in landmarks]            
        known_objectIDs = [id for id in objectIDs if id in landmarks] 
        if len(objectIDs) == 0: 
            objectIDs = None
        return known_objectIDs, known_dists, known_angles
    else:
        return objectIDs, dists, angles

def remove_known(objectIDs, dists, angles, landmarks):
    '''
    Takes 3 correlated lists of IDs, dists and angles and then removes known IDs and
    their correspondning dists and angles based on the list landmarks(known landmarks). 
    '''
    if objectIDs is not None:
        known_dists = [dist for dist, id in zip(dists, objectIDs) if id not in landmarks]
        known_angles = [angle for angle, id in zip(angles, objectIDs) if id not in landmarks]            
        known_objectIDs = [id for id in objectIDs if id not in landmarks] 
        if len(objectIDs) == 0: 
            objectIDs = None
        return known_objectIDs, known_dists, known_angles
    else:
        return objectIDs, dists, angles

def reset_weight(particle):
    particle.setWeight(0)


###!!!### This function might be the baseline for using the particle filter
def localize():
    #keep turning right with 15 degrees scanning for known landmarks.
    for i in range(24):#24 iterations because 360/15 = 24, so one full rotation
        print(arlo.go_diff(64, 64, 1, 0)) #alternatevely use Mo's rotate
        sleep((0.728/90) * 15)
        print(arlo.stop())
        sleep(0.7)

        #get the next frame. If it seens buggy insert a for loop to get frames multiple times
        frame = cam.get_next_frame() # Read frame
        sleep(0.1)

        objectIDs, dists, angles = cam.detect_aruco_objects(frame)
        objectIDs, dists, angles = remove_unkown(objectIDs, dists, angles, landmarks)
        # We detected atleast one landmark 
        if not isinstance(objectIDs, type(None)):
            for i in range(10): #test how many iterations is needed a good estimated pose
                pass
            #do particle filtering here to localise the robot
            ###Note til Mo, enten lav partikellfilteret om til en funktion og kald det her ellers sæt det her foran partikel filteret.
            ###Så kan vi kalde den her funktion hver gang vi har bevæget os eller sådan, for at finde ud af hvor vi er
            ###Vi kan også prøve at bruge partikel filteret til at vurdere om vi har været tæt nok på en kasse til at sige den er besøgt
            return
    return 

### MAIN PROGRAM ###
try:
    
    # Open windows 
    open_windows()

    # Initialize particles
    particles = initialize_particles(num_particles)

    # The estimate of the robots current pose
    est_pose = particle.estimate_pose(particles) 
    
    # Middlepoint between the two landmarks (GOAL)
    # XXX: center_point = compute_center()

    # Initialize Arlo  
    arlo = robot.Robot()

    # Allocate space for world map
    world = np.zeros((500, 500, 3), dtype = np.uint8)

    # Draw map
    draw_world(est_pose, particles, world)

    print("Opening and initializing camera")
    
    # Check which camera we want to use 
    cam = get_cam()
    
    # Try to selflocalize and get to the center point using the particle filter 
    while 1:

        # Get a pressed key if any for 10 ms. Maybe if removed could boost performance? 
        action = cv2.waitKey(10)
        
        # Quit if we press q 
        if action == ord('q'): 
            break
        
        # Move the robot according to user input (only for testing)
        # control_with_input(action, velocity, angular_velocity)
        
        # TODO: Use motor controls to update particles.
        # TODO: Compute a driving strategy for making sure to see both landmarks. 
        # XXX: Make the robot drive 
        # [particle.move_particle(p, velocity, velocity, angular_velocity) for p in particles]
        
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

        #update objectIDs so that unknown IDs are excluded to insure that the particle filter doesn't fail
        objectIDs, dists, angles = remove_unkown(objectIDs, dists, angles, landmarks)

        # We detected atleast one landmark 
        if not isinstance(objectIDs, type(None)):
            
            # commands.drive(dists[0], 0.3)
            # break
            
            # The total sum of all weigths
            weight_sum = 0.0
            
            # Delete the duplicate if we see the same landmark in one frame 
            objectIDs, dists, angles = delete_duplicates(objectIDs, dists, angles)
            
            #Reset the weights 
            resetWeights = np.vectorize(reset_weight)
            resetWeights(particles)
            print(particles[0].weight)
            print(particles[999].weight)
            #[p.setWeight(0) for p in particles]

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
                p.setWeight(1.0 / num_particles)

        # The estimate of the robots current pose
        est_pose = particle.estimate_pose(particles) 

        # Update the world map 
        update_windows(est_pose, particles, world, frame)
  
# Make sure to clean up even if an exception occurred
finally: 
    clean_up(cam)
