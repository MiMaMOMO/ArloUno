# A2.1 - Obstacle avoidance 

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Robot speed. We use different speed here 
leftSpeed = 60
rightSpeed = 64
rot_speed_front = 1.44
rot_speed_sides = 0.728

for i in range(0, 10000):
    
    front_distance = arlo.read_front_ping_sensor()
    left_distance = arlo.read_left_ping_sensor()
    right_distance = arlo.read_left_ping_sensor()
    
    print(front_distance)
    
    if front_distance <= 500: 
        # Send a go_diff command to drive forward.
        # Rotate right by only driving with the left wheel
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
        
        sleep(rot_speed_front)
        
    if left_distance <= 200:
        # Send a go_diff command to drive forward.
        # Rotate right by only driving with the left wheel
        print(arlo.go_diff(leftSpeed, rightSpeed, 0, 1))
        
        sleep(rot_speed_sides)
        
    if right_distance <= 200:
        # Send a go_diff command to drive forward.
        # Rotate right by only driving with the left wheel
        print(arlo.go_diff(leftSpeed, rightSpeed, 1, 0))
        
        sleep(rot_speed_sides)
    
    # send a go_diff command to drive forward
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))

# Stop Arlo 
print(arlo.stop())
