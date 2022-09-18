# A2.3 - Sampling using SIR (Sampling-Importance-Resampling)

from random import uniform as uf
from scipy.stats import *

def generate_samples():
    '''
    The SIR algorithm. 
    Not complete. Will use other functions for readability. 
    '''
    
    q = []                  # The random sample of q(x)
    sample_bottom = 0.0     # Bottom bound of the range of q
    sample_top = 15.0       # Top bound of the range of q
    k = 20                  # The number of samples in q 
    
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
    
    print(q)
    print('\n')
    
    # Use robot_pose(x) to find the importance_weights by using a distribution from q(x)
    for x in q:
        w.append((x, robot_pose(x) / x))
        
    return w
    
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

print(importance_weights())
