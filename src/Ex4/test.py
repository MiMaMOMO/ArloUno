import numpy as np 

angle = 1.57079
dist = 100.0

cos_x = np.cos(angle)
sin_y = np.sin(angle)

updated_x = 206.0 + (dist * cos_x)
updated_y = 51.0 + (dist * sin_y)
updated_theta = angle

print("Cos(x):  {}".format(cos_x))
print("Sin(y):  {}".format(sin_y))
print("x:       {}".format(updated_x))
print("y:       {}".format(updated_y))
