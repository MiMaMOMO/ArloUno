import numpy as np 
from settings import * 

angle_x = 3.14159
angle_y = 1.57079
dist = 100.0
ori = 0.0
x = -100.0
y = 0.0

def test(angle, dist, current_x, current_y):
    
    cos_x = np.cos(angle)
    sin_y = np.sin(angle)
    
    if theta <= DEGREES_180 and theta >= 0:
        x = current_x - (-dist * cos_x)
        y = current_y + (dist * sin_y)
    elif theta > DEGREES_180 and theta <= DEGREES_360:
        x = current_x + (dist * cos_x)
        y = current_y - (-dist * sin_y)
        
    return x, y 

def new_position(angle, dist, x, y):
    # Compute the unit vector of our orientation in radians
    cos_x = np.cos(angle)
    sin_y = np.sin(angle)

    if angle <= 1.57079 and angle >= 0:
        print("1!")
        updated_x = x - (-dist * cos_x)
        updated_y = y + (dist * sin_y)
    elif angle > 1.57079 and angle <= 3.14159:
        print("2!")
        updated_x = x - (-dist * cos_x)
        updated_y = y + (dist * sin_y)
    elif angle > 3.14159 and angle <= 4.721388:
        print("3!")
        updated_x = x - (-dist * cos_x)
        updated_y = y - (-dist * sin_y)
    elif angle > 4.721388 and angle < 6.292:
        print("4!")
        updated_x = x + (dist * cos_x)
        updated_y = y - (-dist * sin_y)
        
    return updated_x, updated_y


cos_x = np.cos(angle_x)
sin_y = np.sin(angle_x)

updated_t = angle_x + angle_x
theta = np.mod(updated_t, 2.0 * np.pi)

updated_x, updated_y = test(theta, dist, x, y)

# if theta <= 1.57079 and theta >= 0.0:
#     print("1!")
#     updated_x = x + (dist * cos_x)
#     updated_y = y + (dist * sin_y)
# elif theta > 1.57079 and theta <= 3.14159:
#     print("2!")
#     updated_x = x + (dist * cos_x)
#     updated_y = np.abs(y + (dist * sin_y))
# elif theta > 3.14159 and theta <= 4.721388:
#     print("3!")
#     updated_x = -1 * x + (dist * cos_x)
#     updated_y = -1 * y + (dist *  (-1 * sin_y))
# else: 
#     print("4!")
#     updated_x = x + (dist * cos_x)
#     updated_y =  -1 * y + (dist * sin_y)


print("Cos(x):  {}".format(cos_x))
print("Sin(y):  {}".format(sin_y))
print("x:       {}".format(updated_x))
print("y:       {}".format(updated_y))
print("t:       {}".format(theta))
