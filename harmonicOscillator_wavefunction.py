#! /usr/bin/env python3

'''
harmonicOscillator_wavefunction.py is a python script that finds the values of the wavefunction for a 1-d quantum
harmonic oscillator for various energy levels.

Janiris Rodriguez
PHZ 4151C
Mar 4, 2021
'''

import numpy as np
import matplotlib.pyplot as plt
import math

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
# for pt a
n_a = [0,1,2,3]                        # store different values of n to evaluate wavefunction for
x_a = np.linspace(-4,4,1000).tolist()  # list of 1000 x values from -4 to 4 to evaluate value of the wavefunction of nth energy level
wavefunc_a = []                        # list of lists storing values for wavefunction for different n values

# loop over how many different n values we have to find different wavefunction values, for pt a
for i in range(len(n_a)):
    temp_wavefunc = []    # will temporarily store values for wavefunction of n_values[i]th energy level
    for j in range(len(x_a)):
        # loop over all the x values to find value of wavefunction
        temp_wavefunc.append(wavefunction(n_a[i], x_a[j]))
    # after finding all the values of wavefunction for a given n, append to wavefunc_n
    wavefunc_a.append(temp_wavefunc)

# for pt b
n_b = 30
x_b = np.linspace(-10,10,1000).tolist()    # generate 1,000 points from -10 to 10
wavefunc_b = []                            # list to store values of wavefunction for n = 30

# find values of wavefunction in x_b range for n = 30 and store them in a list
for i in range(len(x_b)):
    wavefunc_b.append(wavefunction(n_b, x_b[i]))


# plot the wavefunctions for different energy levels, for pt a
for i in range(len(n_a)):
    plt.plot(x_a, wavefunc_a[i], label = f'n = {n_a[i]}')
plt.xlabel('x')
plt.ylabel('$\Psi_{n}$(x)')
plt.title('Wavefunction for 1d Quantum Harmonic Oscillator\n for Various Energy Levels')
plt.legend(edgecolor = 'white')                   # creates legend
ax = plt.gca()                                    # gets the axes for this specific plot
ax.spines['top'].set_visible(False)               # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('wavefunctionPlot_a.png', format = 'png')   # saves figure
plt.show()
plt.clf()

# plot the wavefunctions for n = 30, for pt b
plt.plot(x_b, wavefunc_b)
plt.xlabel('x')
plt.ylabel('$\Psi_{30}$(x)')
plt.title('Wavefunction for 1d Quantum Harmonic Oscillator\n for n = 30')
ax = plt.gca()                                    # gets the axes for this specific plot
ax.spines['top'].set_visible(False)               # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('wavefunctionPlot_b.png', format = 'png')   # saves figure
plt.show()
plt.clf()
