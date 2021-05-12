#! /usr/bin/env python3

'''
lagrangePoint.py is a python script that finds the distance to the L1 lagrange point from the center of the Earth
using Newton's method to solve the force equation that a satellite would experience at that point.

Janiris Rodriguez
PHZ 4151C
Mar 10, 2021
'''

import scipy.constants as constants

# necessary constants for calculation in SI units
G = constants.G            # Newton's gravitational constant
M = 5.974e24               # mass of Earth
m = 7.348e22               # mass of Moon
R = 3.844e8                # distance between the center of the Earth and the center of the Moon
omega = 2.662e-6           # angular frequency of a satellite at the L1 lagrange point, same as that of the Moon

def f(r):
    '''
        the function to find the zeros of

        input:
            r (float): the distance of an object from the center of Earth
        returns:
            the value of the function for a given distance away from Earth
    '''

    # individually calculating the terms in the equation
    term1 = G * m / (R - r)**2  # gravitational acceleration satellite at L1 experiences from the Moon
    term2 = G * M / r**2        # gravitational acceleration satellite at L1 experiences from the Sun
    term3 = r * omega**2        # resultant acceleration of satellite, centripetal acceleration

    # combining all the terms
    y = term1 - term2 + term3

    return y

def f_prime(r):
    '''
        derivative of the function to find the zeros of

        input:
            r (float): the distance of an object from the center of the Earth
        returns:
            value of derivative for this given r

    '''

    # calculating individual terms in derivative
    term1 = 2.0 * G * m / (R - r)**3
    term2 = 2.0 * G * M / r**3

    # combining these terms
    y = term1 + term2 + omega**2

    return y

def newtonMethod(r_current, targetAccuracy, func, func_prime):
    '''
        finds the zero of a function using Newton's method

        input:
            r_current (float): starting point for Newton's method
            targetAccuracy (float): accuracy to be reached
            func (function): function to find root of
            func_prime (function): derivtaive of the function to find root of
        returns:
            location of the root of function to entered accuracy

    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached
    zero_Found = False

    # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
    while not zero_Found:

        # calculates guess for the location of the root
        term = func(r_current) / func_prime(r_current)
        r_prime = r_current - term

        # check to see if this new r is the root
        if func(r_prime) == 0:
            zero_Found = True

        # calculates the distance between the two points to check if desired accuracy has been reached
        if abs(r_prime - r_current) <= targetAccuracy:
            zero_Found = True

        # set variable to prepare for either for next iteration of loop or to return location of root if desired accuracy was reached
        r_current = r_prime

    return r_current

# main code block
r_start = 6.371e6           # value to start looking for roots from. set it to be radius of earth because location of L1 cannot be inside Earth
desiredAccuracy = 1.0e-7    # target accuracy to get an answer that is right to 4 sig figs

# calculate the location of the L1 lagrange point using Newton's method
L_1 = newtonMethod(r_start, desiredAccuracy, f, f_prime)

print(f'The distance from the center of Earth to the L1 Lagrange point is {L_1:.4e} m')
