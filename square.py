from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 60
rightSpeed = 64
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# Wait a bit while robot moves forward
sleep(3)

# send a stop command
print(arlo.stop())

# Wait a bit before next command
sleep(0.041)

# turn right
print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

# Wait a bit before next command
sleep(1)

# send a stop command
print(arlo.stop())
