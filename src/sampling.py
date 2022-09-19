# A2.3, A2.4 - Sampling using SIR (Sampling-Importance-Resampling)

from random import sample, uniform as uf
from tkinter import Scale
from scipy.stats import *
import numpy as np

# Step 1 - Generate random samples 
def generate_samples():
    '''
    The SIR algorithm. 
    Not complete. Will use other functions for readability. 
    '''
    
    q = []                  # The random sample of q(x)
    sample_bottom = 0.0     # Bottom bound of the range of q
    sample_top = 15.0       # Top bound of the range of q
    k = 200                  # The number of samples in q 
    
    # Step 1, Sampling - q(x) 
    # Populate q by choosing random floats between 0 - 15 
    for _ in range(0, k):
        q.append(uf(sample_bottom, sample_top))
    
    return q

# Step 2 - Calculating the weights of each sample 
def importance_weights():
    '''
    Calculate importance_weights for each sample. 
    '''
    
    q = generate_samples()  # Generate random samples 
    w = []                  # Sample weights 
    
    #print(q)
    #print('\n')
    
    # Use robot_pose(x) to find the importance_weights by using a distribution from q(x)
    for x in q:
        w.append((x, robot_pose(x) / x))
        
    return w
    
# Step 3 - Resampling 
def resample():
    '''
    ...
    '''
    
    # Normalize weigths 
    samples = importance_weights()
    
    q = []
    w = []
    
    for i in samples:
        q.append(i[0])
    
    for i in samples:
        w.append(i[1])
    
    norm_weigths = [float(i)/sum(w) for i in w]
    
    # Generates a random sample from a the normalized weigths 
    np_samples = np.asarray(q)
    np_weigths = np.asarray(norm_weigths)
    resample = np.random.choice(np_samples, len(q), True, np_weigths)
    
    return resample

def robot_pose(x):
    '''
    This uses robot_pose(x) to in the assignment for a normal distribution. This number is used to importance_weights the samples in q(x). 
    
    Parameters:
        x (float) : The value x in the random samples of q.
    '''
    
    # The tree continous normal distributions describing the robots position 
    fst_normal_dist = norm.pdf(x, loc = 2.0, scale = 1.0)
    snd_normal_dist = norm.pdf(x, loc = 5.0, scale = 2.0)
    trd_normal_dist = norm.pdf(x, loc = 9.0, scale = 1.0)
    
    # Calculating robot_pose(x) which is the robots position 
    p = 0.3 * fst_normal_dist + 0.4 * snd_normal_dist + 0.3 * trd_normal_dist
    
    return p

def test(x):
    p = norm.pdf(x, loc = 5, scale = 4)
    
    return p 
    
def test_norm():
    # Normalize weigths 
    samples = importance_weights()
    
    q = []
    w = []
    
    for i in samples:
        q.append(i[0])
    
    for i in samples:
        w.append(i[1])
    
    norm_weigths = [float(i)/sum(w) for i in w]
    
    # Generates a random sample from a the normalized weigths 
    np_samples = np.asarray(q)
    np_weigths = np.asarray(norm_weigths)
    resample = np.random.choice(np_samples, len(q), True, np_weigths)
    
    return resample

print(test_norm())
