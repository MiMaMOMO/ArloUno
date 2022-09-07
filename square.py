from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Speed 
leftSpeed = 60
rightSpeed = 64

for i in range(0, 20):
    # send a go_diff command to drive forward
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

    # Wait a bit while robot moves forward
    sleep(2.52)

    # send a stop command
    print(arlo.stop())

    # Wait a bit before next command
    sleep(0.041)

    # turn right
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))

    # Wait a bit before next command
    sleep(0.72)

    # send a stop command
    print(arlo.stop())
    
    # Wait a bit before next command
    sleep(0.041)
