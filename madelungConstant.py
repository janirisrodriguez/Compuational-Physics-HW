#! /usr/bin/env python3

'''
madelungConstant.py is a python script that calculates the Madelung constant for NaCl with a sodium atom at the
origin by adding all the potentials at the origin of all the other atoms in the lattice.

Janiris Rodriguez
PHZ 4151C
Feb 3, 2021
'''

import numpy as np
import time

# records the time that program starts
start = time.time()

#don't need constants because they cancel out in the end
def potential(x, y, z):
    '''
        calculates the dimensionless potential at the origin due to an atom at (x,y,z)
        input:
            x,y,z (float): coordinates of an atom
        returns:
            dimensionless potential
    '''

    distance = np.sqrt(x**2 + y**2 + z**2)
    V = 1 / distance

    #calculates whether the sum of coordinates is odd to make sure V is negative
    if ((x+y+z) % 2) == 1:
        V *= -1

    return V

#main code block
M = 0
L = 135

#runs through all possible combinations of i,j,k
for i in range(-L,L):
    for j in range(-L,L):
        for k in range(-L,L):

            #this gives a 0 in the denominator
            if i == 0 and j == 0 and k == 0:
                continue

            else:
                M += potential(i,j,k)


tot_Time = time.time() - start

print(f'The Madelung constant for NaCl is {M:.4f}')
print(f'This takes {tot_Time:.2f} s to run')
