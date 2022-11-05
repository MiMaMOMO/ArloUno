import sys 
import numpy as np

sys.path.append("../rally")

import auxiliary
from settings import * 
    

ids = np.array([1, 4, 3, 4, 7])
dists = [432.1, 162.3, 370.5, 22.5, 28.1]
angles = [0.28, 0.56, 0.88, 1.2, 2.1]

# ids, dists, angles = aux.delete_duplicates(ids, dists, angles)
ids, dists, angles = auxiliary.remove_known(ids, dists, angles)

print(ids)
print(dists)
print(angles)
