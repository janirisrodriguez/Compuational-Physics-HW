#! /usr/bin/env python3

'''
specialRelativity.py is a python script that uses special relativity to calculate the time for a spaceship to
travel some user-entered distance at some user-entered relativistic speed as measured by an at rest observer on
Earth (observer A) and as measured by a passenger on the ship (observer B).

Janiris Rodriguez
PHZ 4151C
Mar 1, 2021
'''

import numpy as np

# allow for user input for distance between Earth and planet as measured by observer A and for speed of ship
earth_x = float(input('Distance spaceship must travel (in light-years): '))
v = float(input('Speed of spaceship (as a fraction of c): '))

# calculates gamma factor
inside_sqrt = 1. - v**2
gamma = 1. / np.sqrt(inside_sqrt)

earth_t = earth_x / v            # time as measured by observer A
spaceship_t = earth_t / gamma    # time as measured by observer B

print(f'In the rest frame of an observer on Earth, the trip will take {earth_t:.3f} years')
print(f'In the frame of an observer on the spaceship, the trip will take {spaceship_t:.3f} years')
