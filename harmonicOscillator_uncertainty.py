#! /usr/bin/env python3

'''
harmonicOscillator_uncertainty.py is a python script that calculates the quantum uncertainty of a particle in a
given energy level of a quantum harmonic oscillator. The integral is evaluated using Gaussian quadrature.

Janiris Rodriguez
PHZ 4151C
Mar 4, 2021
'''

import numpy as np
import matplotlib.pyplot as plt
import math
# contains function to calculate weights and sample points for Gaussian quadrature method - written by Mark Newman
import gaussxw

def gaussianQuadrature(func,a,b,N,*additionalArgs):
    '''
        calculates value of an integral using the Gaussian quadrature method. To calculate the weights for the
        sample points, Simpson's rule is used

        input:
            func (function): user-defined function to integrate over
            a (float): lower limit of integral
            b (float): upper limit of integral
            N (int): number of slices
            *additionalArgs (tuple): additional arguements to be passed into func if func requires more than
                                        one arguement

        returns:
            approximate value of integral
    '''
    I = 0

    # x - sample points
    # w - weights for those sample points
    # calculates the sample points and weights for gaussian quadrature on [-1,1] interval
    x, w = gaussxw.gaussxw(N)

    # map the sample points on domain that is [a,b] and rescaling the weights for this domain
    x_prime = np.zeros(len(x))
    w_prime = np.zeros(len(w))

    for i in range(len(x)):
        x_prime[i] = 0.5*(b - a)*x[i] + 0.5*(b + a)
        w_prime[i] = 0.5*(b - a)*w[i]

    # if function being integrated requires additional arguements
    if additionalArgs:
        # evaluating the integral with the adjusted weights and sample points
        for i in range(len(x)):
            I += w_prime[i]*func(x_prime[i], additionalArgs)

    else:
        # evaluating the integral with the adjusted weights and sample points
        for i in range(len(x)):
            I += w_prime[i]*func(x_prime[i])

    return I

def f(z,n):
    '''
        integrand to find root-mean-square position for 1d harmonic oscillator, change of variable used

        input:
            z (float): integration variable for function, z = x / (1 + x)
            n (tuple of ints): represents energy level for wavefunction, passed in as a tuple

        returns:
            value of function
    '''

    term = 1.0 - z     # term found repeatedly in function, for sake of readability
    arg = z / term     # argument passed into wavefunction function

    # calculate value of wavefunction for given n and z
    wavefunc = wavefunction(n[0],arg)

    # combine all the terms for integrand
    y = 2.0 * (z * wavefunc)**2 / term**4

    return y


def H(n,x):
    '''
        calculates values of the nth Hermite polynomial for a given x value, used to find value of wavefunction

        input:
            n (int): represents the desired Hermite polynomial, H_n, to evaluate
            x (float): value at which the nth Hermite polynomial is being evaluated at

        returns:
            value for H_n(x)
    '''
    # special cases for n = 0 and n = 1, we already know what those two should be so we want to return those in the
    # case that those are the entered n values
    if n == 0:
        Hn_plus = 1.

    elif n == 1:
        Hn_plus = 2 * x

    # when n is not 0 or 1, we actually have to find what the nth Hermite polynomial is
    else:
        # initializing first two Hermite polynomials need to be, set up to find 2nd Hermite polynomial
        Hn_minus = 1
        Hn = 2.0 * x

        n_current = 1  # keeps track of the Hermite polynomial stored in Hn, starts at 1

        # loop until we reach our desired n
        while n != n_current:
            # finding individual terms then combining for sake readability to find the (n_current + 1)th Hermite polynomial
            term1 = 2. * x * Hn
            term2 = 2. * n_current * Hn_minus
            Hn_plus = term1 - term2

            # adjusting variables in the case that n is not the same as n_current in the next iteration of loop
            n_current += 1    # incrementing the counter
            Hn_minus = Hn     # move back the values of Hermite polynomials
            Hn = Hn_plus

    return Hn_plus

def wavefunction(n, x):
    '''
        calculates values of wavefunction of the nth energy level for a 1-d quantum harmonic oscillator

        input:
            n (int): energy level
            x (float): value at which to evaluate the wavefunction of the nth energy level

        returns:
            value of wavefunction
    '''

    # calculate different terms for wavefunction
    denom = 2.0**n * math.factorial(n) * np.sqrt(np.pi)
    exponential = x**2 / 2.0
    hermite = H(n,x)           # find the value of the nth hermite polynomial for given x value

    # combine all the terms
    psi = np.exp(-exponential) * hermite / np.sqrt(denom)

    return psi

# main code block
n = 5             # energy level to find the uncertainty of particle in
num = 100         # number of points to use for Gaussian quadrature
# bounds for integral
lowerLim = 0
upperLim = 1

# calculate root-mean-square position using Gaussian quadrature
rms_x = np.sqrt(gaussianQuadrature(f, lowerLim, upperLim, num, n))

print(f'The quantum uncertainty of a particle in the {n}th level of a quantum harmonic oscillator is {rms_x:.2f}')
