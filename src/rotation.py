## Testing rotation for Arlo for 90 deegres

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Arlo speed. We use the same speed here 
leftSpeed = 64
rightSpeed = 64

# Send a go_diff command to drive forward.
# Rotate right by only driving with the left wheel
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# The time Arlo have to rotate 90 deegrees before the next command 
sleep(0.728)

# Stop Arlo 
print(arlo.stop())

# Wait a bit before next command
sleep(0.041)