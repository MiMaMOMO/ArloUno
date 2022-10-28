import numpy as np 

angle_x = 3.14159
angle_y = 1.57079
dist = 100.0

cos_x = np.cos(angle_y)
sin_y = np.sin(angle_y)

# 0.0, 0.0

updated_x = 0.0 - (dist * cos_x)
updated_y = 100.0 - (dist * sin_y)

print("Cos(x):  {}".format(cos_x))
print("Sin(y):  {}".format(sin_y))
print("x:       {}".format(updated_x))
print("y:       {}".format(updated_y))
