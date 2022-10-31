# A1.1) 5x Square exercise 

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Arlo speed. Different speeds
leftSpeed = 60
rightSpeed = 64
rot_speed = 64

# Start the sequence for completing a square five times 
for i in range(0, 20):
    
    # Send a go_diff command to drive forward
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

    # Approximatly one meter of sleep 
    sleep(2.52)

    # Stop Arlo 
    print(arlo.stop())

    # Wait a bit before next command
    sleep(0.041)

    # Turn 90 deegres to the right
    print(arlo.go_diff(rot_speed, rightSpeed, 1, 0))

    # Wait a bit before next command
    sleep(0.69)

    # send a stop command
    print(arlo.stop())
    
    # Wait a bit before next command
    sleep(0.041)
