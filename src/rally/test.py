import numpy as np

from auxiliary import delete_duplicates

from settings import * 


ids = np.array([9 ,9, 9, 5, 5])
dists = np.array([3456.2, 2.3, 2.3, 44.2, 35.6])
angles = np.array([3456.2, 2.3, 4.3, 0.1, 0.7])

ids, dists, angles = delete_duplicates(ids, dists, angles)
                    
shortest_idx = np.where(dists == min(dists))

focused_obstacle_idx = np.where(OBSTACLES_IDS == ids[shortest_idx])[0][0]

real_value = OBSTACLES_IDS[focused_obstacle_idx]

print(ids)
print(dists)
print(angles)
print(shortest_idx)
print(focused_obstacle_idx)
print(real_value)
