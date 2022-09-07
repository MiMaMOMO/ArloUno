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

sleep(10)

print(arlo.stop())

# send a go_diff command to drive forward
print(arlo.go_diff(leftSpeed, rightSpeed, 0, 0))

sleep(10)

print(arlo.stop())
