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
        print("Starting quest towards landmark: {}...".format(LANDMARK_IDS[rute_idx]))
    
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
                    shortest_idx = np.where(dists == min(dists))
                    
                    # Find the index in the list of obstacles ids Arlo is focusing on 
                    obstacle_idx = np.where(OBSTACLES_IDS == obstacle_ids[shortest_idx])[0][0]
                    
                    # Print the chosen obstacle 
                    print("I've chosen to look for obstacle {}.".format(OBSTACLES_IDS[obstacle_idx]))
                
                    # Scan for the specific obstacle with the shortest distance 
                    short_id, short_dist, short_angle = cmds.scan_obstacles(
                        arlo, cam, OBSTACLES_IDS[obstacle_idx])
                    
                    # Print that Arlo will try to move towards the obstacle
                    print("Starting rotation and movement towards obstacle {}.".format(short_id[0]))
                else:
                    # What should happen if Arlo cannot find any obstacles? (highly unlikely)
                    pass
                
                # Move towards the choosen obstacle  
                aux.move_to_box(arlo, cam, short_id, short_dist, short_angle, OBSTACLE_RANGE, OBSTACLES_IDS)
                
                # while 1: 
                    
                #     # Arlo cannot see anything and we assume we are close to the obstacle 
                #     if isinstance(short_id, type(None)):
                #         break
                    
                #     # Rotate towards the obstacle if the angle is bigger than 13 degrees
                #     if np.abs(short_angle[0]) > DEGREES_13:
                #         cmds.rotate(arlo, short_angle[0])
                        
                #     # Find the minimum betwen the distance found and 1m
                #     dist = np.minimum(short_dist[0], ONE_METER)

                #     # Drive within 60cm of the obstacle if the dist < 1.1m,
                #     # otherwise drive the full length
                #     if (short_dist[0] - ONE_METER) <= 10.0:
                #         print("Starting landmark drive with dist = {}".format(short_dist))
                #         cmds.drive(arlo, short_dist[0], OBSTACLE_RANGE)
                #         break
                #     else:
                #         print(
                #             "Starting normal drive with dist = {}".format(short_dist))
                #         cmds.drive(arlo, NORMAL_DRIVE)

                #     # Try and detect the obstacle Arlo are focusing on
                #     # TODO: What if Arlo sees two boxes here? This can happen with landmarks or if Arlo sees two obstacles at the same time. Maybe implement a filter so Arlo only focuses on the focuses obstacle?
                #     short_id, short_dist, short_angle = cmds.detect(cam, OBSTACLES_IDS)
                    
        
        # We detected the landmark Arlo was searching for 
        if not isinstance(objectIDs, type(None)):
            
            # Print that Arlo found the landmark 
            print("I found the landmark I was scanning for.")
            
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
            break
            
            # # Rotating and driving towards the found landmark within a certain range
            # while 1:

            #     # Arlo cannot see anything and we assume we are close to the landmark 
            #     if isinstance(objectIDs, type(None)):
            #         break

            #     # Rotate towards the landmark if the angle is bigger than 13 degrees
            #     if np.abs(angles[0]) > DEGREES_13:
            #         print("Starting rotation with angle = {}".format(angles[0]))
            #         cmds.rotate(arlo, angles[0])

            #     # Find the minimum betwen the distance and 1m
            #     # dist = np.minimum(dists[0], ONE_METER)

            #     # Drive within 40cm of the landmark if the dist <= 1.1m,
            #     # otherwise drive the full length
            #     if (dists[0] - ONE_METER) <= 10.0:
            #         print("Starting landmark drive with dist = {}".format(dists[0]))
            #         cmds.drive(arlo, dists[0], LANDMARK_RANGE)
            #         break
            #     else:
            #         print("Starting normal drive with dist = {}".format(dists[0]))
            #         cmds.drive(arlo, NORMAL_DRIVE)
                    
            #     # Try and detect the landmark Arlo are focusing on
            #     # TODO: What if Arlo sees two boxes here? This will happen with obstacles or if   Arlo sees two landmarks at the same time. Maybe implement a filter so Arlo only focuses on the focuses landmark? 
            #     objectIDs, dists, angles = cmds.detect(cam, LANDMARK_IDS)

        # Print Arlos goal 
        print("Succesfully completed the quest for landmark: {}!".format(LANDMARK_IDS[rute_idx]))

        # Arlo found its way to the landmark so we wanna look for the next landmark 
        rute_idx += 1

    # Stop Arlo just in case he continues after endning the rute 
    arlo.stop()
