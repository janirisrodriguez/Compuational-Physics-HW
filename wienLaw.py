#! /usr/bin/env python3

'''
wienLaw.py is a python script that finds Wien's displacement constant by solving for the solution of the equation that
yields the wavelength at whihch the emitted radiation is the strongest (derivative of intensity of radiation I set
equal to 0) by using the binary search method. It alsouses this value to approximate the temperature of the surface
of the Sun.

Janiris Rodriguez
PHZ 4151C
Mar 9, 2021
'''

import numpy as np
import scipy.constants as constants
import sys

def f(x):
    '''
        function to find zero of

        input:
            x (float): dependent variable. represents hc/[(wavelength)*k_B*T]
        returns:
            value of function at given x value
    '''
    return(5*np.exp(-x) + x - 5.)

def binarySearch(x_1, x_2, epsilon, func):
    '''
        tries to find root of func in between two entered x values using the binary search method

        input:
            x_1 (float): point at which to start search for root
            x_2 (float): point at which to end search for root
            epsilon (float): accuracy to be reached, target distance between the x values
            func (function): function to find root of
        returns:
            either the position of x value if func(x_1) and func(x_2) have opposite signs or an exit if not
    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached
    zero_Found = False

    # checking to make sure that f(x1) and f(x2) have opposite signs. if they do, this division will yield negative number
    # necessary for these two values to have opposite signs for binary search method to work
    if func(x_1)/func(x_2) < 0:

        # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
        while not zero_Found:
            x_prime = (x_1 + x_2) / 2.0         # find midpoint between two values
            f_prime = func(x_prime)

            # check to see if value of function at new x value has same sign as function at either of the two points
            # if they do, replace that original x value with the new value
            if f_prime/func(x_1) > 0:
                x_1 = x_prime
            else:
                x_2 = x_prime

            # calculates the distance between the two points to check if desired accuracy has been reached
            if abs(x_1 - x_2) <= epsilon:
                zero_Found = True

        # after desiredAccuracy has been reached, calculate the midpoint the two x values one more time
        # this is the final estimate for where the zero of the function is
        zero = (x_1 + x_2) / 2.0

        return zero

    # f(x1) and f(x2) start off with the same sign so it's not possible to use binary search to find zero
    else:
        sys.exit('f(x1) and f(x2) have the same sign initially. Binary search method failed.')


# main code block
# initializing necessary constants in SI units
k_B = constants.k      # Boltzmann constant
h = constants.h        # Planck constant
c = constants.c        # speed of light

# setting up what is necessary for binary search method
desiredAccuracy = 1.0e-6       # accuracy to solve equation to
x1 = 0.1                      # initial point at which to start search for zero
x2 = 10.                      # final point at which to start search for zero

# find zero of function, f
soln = binarySearch(x1, x2, desiredAccuracy, f)

# calculate value for displacement constant
b = h * c / (k_B  * soln)

print(f'Wien\'s displacement constant is {b:.3e} m*K')

lambda_peak = 502.0e-9        # wavelength peak of Sun's emitted radiation in m
temp = b / lambda_peak        # use Wien's displacement law to find temperature of Sun in K

print(f'The temperature of the Sun is {temp:.3f} K')
