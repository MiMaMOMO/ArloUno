import numpy as np


def randn(mu, sigma) -> float:
    '''
    Normal random number generator with
    mean mu and standard deviation sigma.
    '''
    
    # Compute the random number 
    return sigma * np.random.randn() + mu
