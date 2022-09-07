from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Speed 
leftSpeed = 60
rightSpeed = 64

# send a go_diff command to drive forward
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

sleep(2.52)

print(arlo.stop())
