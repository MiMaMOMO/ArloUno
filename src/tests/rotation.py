## Testing rotation for Arlo for 90 deegres
import sys

sys.path.append("../rally")
sys.path.append("../robot")

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Arlo speed. We use the same speed here 
leftSpeed = 64
rightSpeed = 64

# Send a go_diff command to drive forward.
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))#right turn

# The time Arlo have to rotate 90 deegrees before the next command 
sleep(0.728) #0.728/90 = 0.008

# Stop Arlo 
print(arlo.stop())

# Wait a bit before next command
sleep(0.041)
