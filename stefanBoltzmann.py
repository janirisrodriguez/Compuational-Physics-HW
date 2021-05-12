#! /usr/bin/env python3

'''
stefanBoltzmann.py is a python script that calculates a value for the Stefan-Boltzmann constant by finding the
total energy per unit area radiated by a black body as a function of T by using adaptive Simpson's rule to evaluate
the integral and then printing out what the constant in front of T is.

Janiris Rodriguez
PHZ 4151C
Mar 3, 2021
'''

import numpy as np

def adaptiveSimpsonsRule(func, a, b, desiredAccuracy, *additionalArgs):
    '''
        integration using the adaptive Simpson's rule method in one dimension

        input:
            func (function): user-defined function to be integrated over
            a (float): lower limit of integral
            b (float): upper limit of integral
            desiredAccuracy (float): approximate accuracy desired for value of integral
            *additionalArgs (tuple): additional arguements to be passed into func if func requires more than one arguement

        returns:
            approximate value of integral
    '''
    # starting with 1 slice
    N = 1
    # initializing S,T, and the result of the integral, I, for 1 slice
    if additionalArgs:
        S_current = (func(a, additionalArgs) + func(b, additionalArgs)) / 3.
    else:
        S_current = (func(a) + func(b)) / 3.

    T_current = 0
    I_current = (b - a) * S_current

    # imitates do-while loop, breaks out of loop when desired accuracy is achieved
    while True:

        if N != 1:
            # defining spacing for certain slice number
            h_current = (b - a) / N
            # making sure that this term starts at 0 for summation for new number of slices
            T_current = 0

            # sum over k from 1 to N-1 for odd k, adding terms necessary
            if additionalArgs:
                for k in range(1,N,2):
                    T_current += func(a + k*h_current, additionalArgs)
            else:
                for k in range(1,N,2):
                    T_current += func(a + k*h_current)

            # finalizing terms for result of integral for certain slice number
            T_current *= 2/3.
            S_current = S_prev + T_prev
            # result of integral for certain slice number
            I_current = h_current * (S_current + 2*T_current)
            # calculating the approximate accuracy
            epsilon_current = (I_current - I_prev) / 15.

            # checks for whether desired accuracy has been achieved
            if abs(epsilon_current) <= abs(desiredAccuracy):
                break

        # increments step and establishes variables for next iteration of loop with different slice number
        N *= 2
        T_prev = T_current
        S_prev = S_current
        I_prev = I_current

    return I_current


def f(z, constant):
    '''
       defines the function to integrate, change of variable used
       input:
           z (float): integration variable for funtion, z = x / (x + constant)
           constant (float): constant found for shift in change of variable
        returns:
            value of function for given x and constant values
    '''
    # calculate the individual terms needed for sake of readability
    term1 = z**3
    term2 = 1. - z

    exponential_num = constant[0] * z
    term3 = np.exp(exponential_num / term2) - 1.

    # combine all the terms together
    y = term1 / term2**5
    y /= term3

    return y

# main code block
# necessary constants in SI units
k_B = 1.38064852e-23     # boltzmann constant
c = 3.0e8                # speed of light
hbar = 1.054571817e-34   # planck constant / 2*pi

# constant used when changing variables to ensure peak of function falls in middle of integration range for accuracy
shift = 2.94753090254

# find constant in front of integral
const_denom = 4. * (np.pi)**2 * c**2 * hbar**3
const_num = (shift * k_B)**4
const = const_num / const_denom

# bounds to integrate over, want to be close to 0 and 1, but those result in divide by 0 error
lowerLim = 0.000000000000001
upperLim = 0.999999999999999

# desired accuracy for integral
epsilon = 1.0e-11

# find value of integral using adaptive Simpson's rule
integral = adaptiveSimpsonsRule(f, lowerLim, upperLim, epsilon, shift)

# find stefan-boltzmann constant
sigma = const * integral

print(f'Stefan-Boltzmann constant: {sigma:.2e}')
