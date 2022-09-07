# A1.2) Exercise for creating an eigth

from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Speed 
leftSpeed = 64
rightSpeed = 64
rot_speed_right = 32
rot_speed_left = 32
sleep_rot_first = 11.8
sleep_rot_sec = 12.6

for i in range(0, 20):

    # send a go_diff command to drive forward
    #print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

    # Wait a bit while robot moves forward
    #sleep(2.52)

    # Wait a bit before next command
    #sleep(0.041)

    # turn right
    print(arlo.go_diff(leftSpeed, rot_speed_right, 1, 1))

    # Wait a bit before next command
    sleep(sleep_rot_first)
    
    # Wait a bit before next command
    sleep(0.041)
    
    # turn right
    print(arlo.go_diff(rot_speed_left,  rightSpeed, 1, 1))
    
    sleep(sleep_rot_sec)
    
    # Wait a bit before next command
    sleep(0.041)
    
    # send a go_diff command to drive forward
    #print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

    # Wait a bit while robot moves forward
    #sleep(2.52)

    # Wait a bit before next command
    #sleep(0.041)
    

    # Wait a bit before next command

