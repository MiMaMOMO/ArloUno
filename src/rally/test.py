import numpy as np 
from settings import * 

angle_x = 3.14159
angle_y = 1.57079
_test = 1.39626
dist = 100.0
ori = 2.79252
x = -76.9
y = 132.0

def test(angle, dist, current_x, current_y):
    
    cos_x = np.cos(angle)
    sin_y = np.sin(angle)
    
    # if angle <= DEGREES_180 and angle >= 0:
    #     x = particle.getX() - (-dist * cos_x)
    #     y = particle.getY() + (dist * sin_y)
    # elif angle > DEGREES_180 and angle <= DEGREES_360:
    #     x = particle.getX() + (dist * cos_x)
    #     y = particle.getY() - (-dist * sin_y)
        
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


cos_x = np.cos(_test)
sin_y = np.sin(_test)

updated_t = _test + ori
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


def delete_duplicates(objectIDs, dists, angles) -> tuple:
    '''
    Find and delete the duplicates and choose the right ones depending on 
    the shortest distance.
    
    Parameters:
        objectIDs(array)        : Found landmarks.
        dists(array)            : Aruco distances. 
        angles(array)           : Aruco landmarks angles. 
    '''

    # Find the dupplicate items 
    duplicates = [ID for idx, ID in enumerate(objectIDs) if ID in objectIDs[:idx]]

    # Remove the duplicated landmarks at random if any was found 
    if duplicates:
        
        # Traverse the duplicates for comparison 
        for duplicate in duplicates:
            
            # Find all index values having the duplicate 
            duplicate_indexes = np.where(objectIDs == duplicate)
            idx_to_delete = 0
            
            # Find shortest distance between the two duplicates 
            if dists[duplicate_indexes[0][0]] < dists[duplicate_indexes[0][1]]: 
                idx_to_delete = duplicate_indexes[0][1]
            else: 
                idx_to_delete = duplicate_indexes[0][0]
            
            # Delete the further distance values found 
            objectIDs = np.delete(objectIDs, idx_to_delete)
            dists = np.delete(dists, idx_to_delete)
            angles = np.delete(angles, idx_to_delete)

    return objectIDs, dists, angles

ids = np.array([1, 4, 1, 4, 3])
dists = [432.1, 162.3, 370.5, 22.5, 28.1]
angles = [0.28, 0.56, 0.88, 1.2, 2.1]

ids, dists, angles = delete_duplicates(ids, dists, angles)

print(ids)
print(dists)
print(angles)

# print(dists[0:len(ids)])

# print("Cos(x):  {}".format(cos_x))
# print("Sin(y):  {}".format(sin_y))
# print("x:       {}".format(updated_x))
# print("y:       {}".format(updated_y))
# print("t:       {}".format(theta))
