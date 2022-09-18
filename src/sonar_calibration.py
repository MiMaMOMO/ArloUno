# A2.2 - Sonar callibration 

import robot

from time import sleep

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")

# Data findings 
# Distance from BOX. True distance = 0.5m, Arlo distance = 504mm, Afvigelse 4mm
# Distance from BOX. True distance = 1m, Arlo distance = 998mm, Afvigelse 2mm
# Distance from BOX. True distance = 1.5m, Arlo distance = 1503mm, Afvigelse 3mm
# Distance from BOX. True distance = 2.2m, Arlo distance = 2223mm, Afvigelse 3mm
# Distance from BOX. True distance = 3m, Arlo distance = 2406mm, Afvigelse 594mm
# Distance from DOOR. True distance = 0.15m, Arlo distance = 136mm, Afvigelse 14mm
# Distance from DOOR. True distance = 1m, Arlo distance = 1005mm, Afvigelse 5mm
# Distance from DOOR. True distance = 1.8m, Arlo distance = 1635mm, Afvigelse 165mm
# Distance from DOOR. True distance = 2.5m, Arlo distance = 2278, Afvigelse 222mm
# Distance from DOOR. True distance = 3m, Arlo distance = 2700mm, Afvigelse 300mm
# Distance from TABLELEG. True distance = 0.5m, Arlo distance = 54mm, Afvigelse 4mm
# Distance from TABLELEG. True distance = 1m, Arlo distance = 1010mm, Afvigelse 10mm
# Distance from TABLELEG. True distance = 1.5m, Arlo distance = 1489mm, Afvigelse 11mm
# Distance from TABLELEG. True distance = 2.5m, Arlo distance = 2101mm, Afvigelse 399mm
# Distance from TABLELEG. True distance = 3m, Arlo distance = 2448mm, Afvigelse 552mm
# Distance from LEG. True distance = 0.5m, Arlo distance = 44mm, Afvigelse 6mm
# Distance from LEG. True distance = 1m, Arlo distance = 911mm, Afvigelse 89mm
# Distance from LEG. True distance = 1.6m, Arlo distance = 1522mm, Afvigelse 78mm
# Distance from LEG. True distance = 2.4m, Arlo distance = 1982mm, Afvigelse 418mm
# Distance from LEG. True distance = 3m, Arlo distance = 2350mm, Afvigelse 650mm

### The closer Arlo is to an object the better presicion, The further away the less precision. ###

# Run testing  
while 1:
    
    # Read Arlos front distance sensor 
    front_distance = arlo.read_front_ping_sensor()
    
    # Print the distance out 
    print(front_distance)
