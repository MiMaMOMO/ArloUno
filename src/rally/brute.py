# import sys
# import auxiliary
# import commands

# import numpy as np

# from settings import * 


# if ON_ROBOT:
#     sys.path.append("../robot")
    
# # Try to import robot module
# try:
#     import robot
#     ON_ROBOT = True
# except ImportError:
#     print("selflocalize.py: robot module not present - forcing not running on Arlo!")
#     ON_ROBOT = False
    

# def run_brute() -> None:
#     '''
#     Run the brute program where we assume no obstacles. 
#     '''
    
#     # Open windows
#     auxiliary.open_windows()

#     # Initialize Arlo
#     arlo = robot.Robot()

#     # Check which camera we want to use
#     cam = auxiliary.get_cam()

#     # Which known landmark Arlo will search for 
#     rute_idx = 0
    
#     while 1: 
        
#         # We are back at landmark 1 stop the program 
#         if rute_idx >= 5:
#             break
    
#         # Try and detect the first landmark upon starting 
#         # objectIDs, dists, angles, frame = commands.detect(cam)
#         objectIDs, dists, angles, frame = commands.scan(arlo, cam, RUTE[rute_idx])
        
#         # We detected atleast one landmark
#         if not isinstance(objectIDs, type(None)):
            
#             # List detected objects
#             for i in range(len(objectIDs)):
#                 print(
#                     "Object IDs = ", objectIDs[i],
#                     ", Distances = ", dists[i], 
#                     ", Angles = ", angles[i]    
#                 )
            
#             # Rotating and driving towards the found landmark within a certain range
#             while 1:

#                 # We cannot see anything and we assume we are close to the landmark 
#                 if isinstance(objectIDs, type(None)):
#                     break

#                 # Rotate towards the landmark if the angle is bigger than 13 degrees
#                 if np.abs(angles[0]) > DEGREES_13:
#                     print("Starting rotation with angle = {}".format(angles[0]))
#                     commands.rotate(arlo, angles[0])

#                 # Find the minimum betwen the distance and 1m
#                 dist = np.minimum(dists[0], ONE_METER)
                
#                 print(dist)
#                 print(dists[0])
#                 # if dist < ONE_METER or (dists[0] - ONE_METER) <= 30.0: 

#                 # Drive within 40cm of the landmark if the dist < 1m,
#                 # otherwise drive the full length
#                 if (dists[0] - ONE_METER) <= 25.0:
#                     print("Starting landmark drive with dist = {}".format(dist))
#                     commands.drive(arlo, dists[0], LANDMARK_RANGE)
#                     break
#                 else:
#                     print("Starting normal drive with dist = {}".format(dist))
#                     commands.drive(arlo, dist)
                    
#                 # Try and detect the landmark Arlo are focusing on
#                 objectIDs, dists, angles, frame = commands.detect(cam)

#             # Arlo found its way to the landmark so we wanna look for the next landmark 
#             rute_idx += 1

#             # Draw detected objects
#             cam.draw_aruco_objects(frame)

#     # Make sure to clean up even if an exception occurred
#     auxiliary.clean_up(cam)


# ### STARTING POINT OF THE PROGRAM ### 
# if __name__ == '__main__':
#     run_brute()
