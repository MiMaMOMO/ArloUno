# A1.2) Exercise for creating an eigth

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Speed 
leftSpeed = 64
rightSpeed = 64
rot_speed_right = 32
rot_speed_left = 32
sleep_rot_first = 10.53
sleep_rot_sec = 12.35

# Start sequence for continously driving in an eigth pattern
for i in range(0, 20):

    # Start by rotating right by lowering right wheel power 
    print(arlo.go_diff(leftSpeed, rot_speed_right, 1, 1))

    # Wait a bit before next command
    sleep(sleep_rot_first)
    
    # Wait a bit before next command
    sleep(0.041)
    
    # Next turn len when Arlo have completed a 180 deegres rotation 
    print(arlo.go_diff(rot_speed_left, rightSpeed, 1, 1))
    
    # Amount of time Arlo have to complete the turn 
    sleep(sleep_rot_sec)
    
    # Wait a bit before next command
    sleep(0.041)
    