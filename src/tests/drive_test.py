import sys

from rally.commands import rotate, drive
from rally.settings import * 

if ON_ROBOT:
    sys.path.append("../robot")
    
# Try to import robot module
try:
    import robot
    ON_ROBOT = True
except ImportError:
    print("selflocalize.py: robot module not present - forcing not running on Arlo!")
    ON_ROBOT = False

# Create a robot object and initialize
arlo = robot.Robot()
