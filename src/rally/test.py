import sys 
import numpy as np

sys.path.append("../rally")

import auxiliary
from settings import * 
    

ids = np.array([6, 5, 9])
dists = np.array([432.1, 431.0, 402.3])
angles = np.array([0.28, 0.29, 0.30])

print(np.where(dists == min(dists)))

# ids, dists, angles = aux.delete_duplicates(ids, dists, angles)
# ids, dists, angles = auxiliary.delete_duplicates(ids, dists, angles)

# print(ids)
# print(dists)
# print(angles)
