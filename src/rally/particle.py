import numpy as np
import random_numbers as rn

from settings import * 


class Particle(object):
    '''
    Data structure for storing particle information (state and weight). 
    '''
    def __init__(self, x = 0.0, y = 0.0, theta = 0.0, weight = 0.0):
        self.x = x
        self.y = y
        self.theta = np.mod(theta, 2.0 * np.pi)
        self.weight = weight

    def getX(self) -> float:
        return self.x
        
    def getY(self) -> float:
        return self.y
        
    def getTheta(self) -> float:
        return self.theta
        
    def getWeight(self) -> float:
        return self.weight

    def setX(self, val) -> None:
        self.x = val

    def setY(self, val) -> None:
        self.y = val

    def setTheta(self, val) -> None:
        self.theta = np.mod(val, 2.0 * np.pi)

    def setWeight(self, val) -> None:
        self.weight = val


def estimate_pose(particles_list) -> Particle:
    '''
    Estimate the pose from particles by computing the average position and orientation over all particles. This is not done using the particle weights, but just the sample distribution.
    
    Parameters:
        particle_list(array)    :   Numpy array of particles. 
    '''
    
    x_sum = 0.0                     # The sum of all x positions
    y_sum = 0.0                     # The sum of all y positions
    cos_sum = 0.0                   # The sum of all cosinus of the orientation 
    sin_sum = 0.0                   # The sum of all sinus of the orientation 
    flen = len(particles_list)      # The length of our particle array 
    
    # TODO: Numpy this by using np.sum or something 
    for particle in particles_list:
        x_sum += particle.getX()
        y_sum += particle.getY()
        cos_sum += np.cos(particle.getTheta())
        sin_sum += np.sin(particle.getTheta())
        
    # Find the mean value for Arlos particle by using the rest of the particles 
    if flen != 0:
        x = x_sum / flen
        y = y_sum / flen
        theta = np.arctan2(sin_sum / flen, cos_sum / flen)
    else:
        x = x_sum
        y = y_sum
        theta = 0.0
        
    return Particle(x, y, theta)
     
     
def move_particle(particle, delta_x, delta_y, delta_theta) -> None:
    '''
    Move the particle by the new values. 
    
    Parameters: 
        particle(obj)   :   The particle to move. 
        x(float)        :   The particles x coordinate. 
        y(float)        :   The particles y coordinate. 
        theta(float)    :   The particles orientation. 
    '''
    
    # Update the particles values 
    particle.x = delta_x
    particle.y = delta_y
    particle.theta = delta_theta
    
    
def add_uncertainty(particles_list, sigma, sigma_theta) -> None:
    '''
    Add some noise to each particle in the list.
    
    Parameters:
        particle_list(array)    : Numpy array of particles. 
        sigma(float)            : Noise variance for position. 
        sigma_theta(float)      : Noise variance for orientation. 
    '''
    
    # TODO: Numpy this 
    # Add random noise between values 
    for particle in particles_list:
        particle.x += rn.randn(0.0, sigma)
        particle.y += rn.randn(0.0, sigma)
        particle.theta = np.mod(particle.theta + rn.randn(0.0, sigma_theta), 2.0 * np.pi) 


def initialize_particles(num_particles) -> np.ndarray:
    '''
    Initialize a set of particles in a numpy array. 
    
    Parameters: 
        num_particles(int)      : The number of particles we want. 
    '''
    
    # Initialize empty numpy array with enough space and proper data type 
    particles = np.empty(num_particles, dtype = type(Particle))

    # TODO: Numpy this loop. The numbers 100 and 250 should maybe change to offset 
    # Random starting points for each particle
    for i in range(num_particles):
        p = Particle(
            600.0 * np.random.ranf() - 100.0,
            600.0 * np.random.ranf() - 250.0,
            np.mod(2.0 * np.pi * np.random.ranf(), 2.0 * np.pi),
            1.0 / num_particles
        )

        # Replace the empty value with the particle 
        particles[i] = p

    return particles


def new_position(particle, angle, dist) -> tuple:
    '''
    Computes the new x, y and theta value for a particle after movement. 
    
    Parameters: 
        angle(float)            : The amount of angle we want to move.
        dist(float)             : The amount of distance we want to move.  
        current_x(float)        : The particles current x position. 
        current_y(float)        : The particles current y position. 
        current_theta(float)    : The particles current theta orientation. 
    '''
    
    # Compute the new orientation 
    theta = np.mod(angle + particle.getTheta(), 2.0 * np.pi)
    
    # Compute the unit vector of the new orientation in radians 
    cos_x = np.cos(theta)
    sin_y = np.sin(theta)
    
    # Compute the new x and y coordinate for the particle 
    x = particle.getX() + (dist * cos_x)
    y = particle.getY() + (dist * sin_y)
    
    return x, y, theta


def move_all_particles(particles, dist, angle) -> None: 
    '''
    Will update each particle in the digital world depending on where 
    Arlo moves and orientates. 
    
    Parameters:
        particles(ndarray)      : The array of particles. 
        dist(float)             : The distance Arlo went.
        angle(float)            : The angle Arlo used.
    '''
    
    # TODO: Numpy this 
    # Compute each particles new x, y and theta value 
    for p in particles:
        x, y, theta = new_position(p, angle, dist)
        
        # Move the particle to its new coordinate with a new orientation 
        move_particle(p, x, y, theta)
        