# Testing settings for Arlo for 1 meter 

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Robot speed. We use different speed here 
leftSpeed = 60
rightSpeed = 64


for i in range(0, 100):
    
    front_distance = arlo.read_front_ping_sensor() / 1000
    
    if front_distance < 1: 
        # Send a go_diff command to drive forward.
        # Rotate right by only driving with the left wheel
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
        
        sleep(3)
    
    # send a go_diff command to drive forward
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

    # The time the robot have to drive 1 meter 
    sleep(3)

    # Stop the robot 
    print(arlo.stop())
