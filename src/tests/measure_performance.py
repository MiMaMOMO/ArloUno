import timeit
import numpy as np
import time
from rally.particle import initialize_particles


def fun_one():
    '''
    The first function we test. 
    You can write anything in here you want to measure VS. fun_two. 
    '''
    pass


def fun_two():
    '''
    The second function we test.
    You can write anything in here you want to measure VS. fun_one. 
    '''
    pass


# Use this if you wanne test particles 
particles = initialize_particles(5000)

# Initiate a timer 
st = time.time()
 
 # Call the functions 
fun_one()
fun_two()

exe_number = 10
repeat_number = 1


# Measure the execution speed of the first function 
fun_one_time = np.average(timeit.repeat(
    'fun_one()', 
    number = exe_number, 
    repeat = repeat_number, 
    setup = 'from __main__ import fun_one'
    )
)

# Measure the execution speed of the second function 
fun_two_time = np.average(timeit.repeat(
    'fun_two()', 
    number = exe_number, 
    repeat=repeat_number,
    setup = 'from __main__ import fun_two'
    )
)


# Print the seconds it took for each function 
print(f'Function one:       {fun_one_time} seconds')
print(f'Function two:       {fun_two_time} seconds')


# Determine the fastest method of looping
fastest_time = min(fun_one_time, fun_two_time)
fasted_method = 'Function one' if fastest_time == fun_one_time else 'Function two' if fastest_time == fun_two_time else None

print(f'\nThe fastest method is {fasted_method} with {fastest_time} seconds')
