import timeit
import numpy as np
import time
import particle

particles = particle.initialize_particles(5000)

def fun_one():
    x_sum = 0.0
    y_sum = 0.0
    cos_sum = 0.0
    sin_sum = 0.0
    
    for particle in particles:
        x_sum += particle.getX()
        y_sum += particle.getY()
        cos_sum += np.cos(particle.getTheta())
        sin_sum += np.sin(particle.getTheta())


def fun_two():
    x_sum = np.sum(np.fromiter((p.getX() for p in particles), float))
    y_sum = np.sum(np.fromiter((p.getY() for p in particles), float))
    cos_sum = np.sum(np.fromiter((np.cos(p.getTheta()) for p in particles), float))
    sin_sum = np.sum(np.fromiter((np.sin(p.getTheta()) for p in particles), float))

st = time.time()
 
fun_one()
fun_two()

# Measure the execution speed
fun_one_time = np.average(timeit.repeat(
    'fun_one()', number=1, repeat=1, setup='from __main__ import fun_one'))
fun_two_time = np.average(timeit.repeat(
    'fun_two()', number=1, repeat=1, setup='from __main__ import fun_two'))

print(f'Function one:       {fun_one_time} seconds')
print(f'Function two:       {fun_two_time} seconds')

# Determine the fastest method of looping
fastest_time = min(fun_one_time, fun_two_time)
fasted_method = 'Function one' if fastest_time == fun_one_time else 'Function two' if fastest_time == fun_two_time else None

print(f'\nThe fastest method is {fasted_method} with {fastest_time} seconds')
