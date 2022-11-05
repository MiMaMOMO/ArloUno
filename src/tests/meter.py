# Testing settings for Arlo for 1 meter 
import sys

sys.path.append("../rally")
sys.path.append("../robot")

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Robot speed. We use different speed here 
leftSpeed = 60
rightSpeed = 65

# send a go_diff command to drive forward
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# The time the robot have to drive 1 meter 
sleep(2.52)

# Stop the robot 
print(arlo.stop())
