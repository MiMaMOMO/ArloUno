from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Speed 
leftSpeed = 62
rightSpeed = 64

# send a go_diff command to drive forward
# turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# Wait a bit before next command
sleep(0.75)

# send a stop command
print(arlo.stop())

# Wait a bit before next command
sleep(0.041)
