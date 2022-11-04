import numpy as np 

from rally.settings import * 
from rally.auxiliary import delete_duplicates


ids = np.array([1, 4, 1, 4, 3])
dists = [432.1, 162.3, 370.5, 22.5, 28.1]
angles = [0.28, 0.56, 0.88, 1.2, 2.1]

ids, dists, angles =  delete_duplicates(ids, dists, angles)

print(ids)
print(dists)
print(angles)
