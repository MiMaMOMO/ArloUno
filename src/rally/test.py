import sys 
import numpy as np

sys.path.append("../rally")

import auxiliary
from settings import * 
    

ids = np.array([6])
dists = np.array([432.1])
angles = np.array([0.28])

print(len(ids))

# ids, dists, angles = aux.delete_duplicates(ids, dists, angles)
ids, dists, angles = auxiliary.remove_unknown(ids, dists, angles)

print(ids)
print(dists)
print(angles)

print(len(ids))
