import sys

# Appen the robot path 
sys.path.append("../robot")

import auxiliary as aux
import commands as cmds
import numpy as np

from settings import * 


# if ON_ROBOT:
    
# Try to import robot module
# try:
import robot
    # ON_ROBOT = True
# except ImportError:
#     print("selflocalize.py: robot module not present - forcing not running on Arlo!")
#     ON_ROBOT = False
    

def run_brute() -> None:
    '''
    Run the brute program where we assume no obstacles. 
    '''

    arlo = robot.Robot()                    # Instantiate Arlo
    cam = aux.get_cam()                     # Instantiate the camera we will use 
    rute_idx = 0                            # The index of the current goal 
    
    # Start the landmark rute. The program comes here after visiting each landmark 
    while 1: 
        
        # We are back at landmark 1 stop the program 
        if rute_idx >= 5:
            break
        
        # Print Arlos goal 
        print("Starting quest towards landmark: {}...".format(RUTE[rute_idx]))
    
        # Scan for the landmark Arlo is currently focusing on,
        # otherwise use the obstacle strategy and scan for those 
        while 1: 
            
            # Print scanning 
            print("Starting scanning for landmark: {}...".format(RUTE[rute_idx]))
            
            # Arlo starts by scanning for the focused landmark 
            objectIDs, dists, angles = cmds.scan_landmarks(arlo, cam, RUTE[rute_idx])
            
            # Arlo found the landmark so break the loop 
            if not isinstance(objectIDs, type(None)):
                print("I found the landmark.")
                break
            
            # Nothing was found from the landmark scan. Scan for obstacles and store data 
            if isinstance(objectIDs, type(None)): 
                
                # Print the scanning for obstacles 
                print("I did not find landmark {}. Starting scanning for obstacles.".format(RUTE[rute_idx]))
                
                # Start scanning for obstacles 
                obstacle_ids, obstacle_dists, obstacle_angles = cmds.scan_obstacles(arlo, cam)
                
                # Arlo found atleast one obstalce so try to remove duplications 
                if not isinstance(obstacle_ids, type(None)): 
                    
                    obstacle_ids, obstacle_dists, obstacle_angles = aux.delete_duplicates(
                        obstacle_ids, obstacle_dists, obstacle_angles)
                    
                    # Print found obstacles 
                    print("I found {} obstacles.".format(len(obstacle_ids)))
                    
                    # Print the found values out after deleting duplicates 
                    for i in range(len(obstacle_ids)):
                        print(
                            "Object IDs = ", obstacle_ids[i],
                            ", Distances = ", obstacle_dists[i], 
                            ", Angles = ", obstacle_angles[i]    
                        )
                    
                    # Choose the obstacle with the shortest distance
                    # shortest_idx = np.where(obstacle_dists == min(obstacle_dists))
                    
                    # Find the index in the list of obstacles ids Arlo is focusing on 
                    # obstacle_idx = np.where(OBSTACLES_IDS == obstacle_ids[shortest_idx])[0][0]
                    
                    # Print the chosen obstacle 
                    print("I've chosen to look for obstacle {}.".format(obstacle_ids[0]))
                
                    # Scan for the specific obstacle with the shortest distance 
                    # short_id, short_dist, short_angle = cmds.scan_obstacles(
                    #     arlo, cam, OBSTACLES_IDS[obstacle_idx])
                    
                    # Print that Arlo will try to move towards the obstacle
                    print("Starting rotation and movement towards obstacle {}.".format(obstacle_ids[0]))
                    
                    # Move towards the choosen obstacle  
                    aux.move_to_box(arlo, cam, obstacle_ids, obstacle_dists, obstacle_angles, OBSTACLE_RANGE, OBSTACLES_IDS)
                    
                    # 
        
        # We detected the landmark Arlo was searching for 
        if not isinstance(objectIDs, type(None)):
            
            # Print that Arlo found the landmark 
            print("I found the landmark I was scanning for.")
            
            # Filter out the landmarks we arent searching for 
            if len(objectIDs) > 1:
                objectIDs, dists, angles = aux.filter_out(objectIDs, dists, angles, [RUTE[rute_idx]])
                
            # List detected objects
            for i in range(len(objectIDs)):
                print(
                    "Object IDs = ", objectIDs[i],
                    ", Distances = ", dists[i], 
                    ", Angles = ", angles[i]    
                )
                
            # Print that Arlo will try to move towards the landmark 
            print("Starting rotation and movement towards landmark {}.".format(objectIDs[0]))
                
            # Move towards the choosen landmark 
            aux.move_to_box(arlo, cam, objectIDs, dists, angles, LANDMARK_RANGE, LANDMARK_IDS)

        # Print Arlos goal 
        print("Succesfully completed the quest for landmark: {}!".format(LANDMARK_IDS[rute_idx]))

        # Arlo found its way to the landmark so we wanna look for the next landmark 
        rute_idx += 1

    # Stop Arlo just in case he continues after endning the rute 
    # arlo.stop()
