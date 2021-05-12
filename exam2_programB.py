#! /usr/bin/env python3

'''
exam2_programB.py is a python script that solves Schrodinger's equation with a V=x^2
potential for the ground state by using the secant method. It also finds the normalization factor, renormalizes the wavefunction,
graphs the normalized wavefunction and determines the expectation value of x^2.

Janiris Rodriguez
PHZ 4151C
Apr 16, 2021
'''

import numpy as np
import matplotlib.pyplot as plt
import math, sys


def fourthOrderRungeKutta(schrodinger, r, t, h, E):
    '''
        implementation of the fourth order Runge-Kutta method of solving differential equations

        input:
            schrodinger (function): differential equation in terms of r and t
            r (array of floats): values of psi and phi in the first order equations from Schrodinger's
            t (float):  value wavefunction is being evaluated at
            h (float): spacing
            E (float): guess of energy eigenvalue, necessary to evaluate f

        returns:
            solution(s) to the differential equation f

    '''

    k1 = h * schrodinger(r, t, E)
    k2 = h * schrodinger(r+0.5*k1, t+0.5*h, E)
    k3 = h * schrodinger(r+0.5*k2, t+0.5*h, E)
    k4 = h * schrodinger(r+k3, t+h, E)

    soln = (k1 + 2*k2 + 2*k3 + k4) / 6.

    return soln


def schrodinger(r, x, E):
    '''
        represents Schrodinger's equation as 2 first order differential equation

        input:
            r (array of floats): values of psi and phi in the first order equations
            x (float): value the potential will be evaluated at
            E (float): guess of energy eigenvalue

        returns:
            array of floats that represents the values of the two first order differential eqns from Schrodinger's
    '''
    # m = 9.1094e-31      mass of electron
    # hbar = 1.0546e-34   planck's constant, hbar
    # in natural units: hbar^2/m = 1

    # set values equal to their respective variables to solve the 2 first order differential
    # equations from the 1 second order schrodinger enquation
    psi = r[0]
    phi = r[1]

    # the 2 first order differential equations numerocally solved
    fpsi = phi
    fphi = 2.0*(V(x) - E)*psi

    # return the values of the 2 differential equations as an array of floats
    return np.array([fpsi, fphi], float)

def waveFunction(r, schrodinger, xpoints, h, E):
    '''
        function to solve wavefunction

        input:
            r (array of floats): values of psi and phi in the first order equations
            schrodinger (function): differential equation in terms of r and x
            xpoints (array of floats): values of x to evaluate wavefunction at
            h (float): spacing
            E (float): guess of energy eigenvalue

        returns:
            array of points of the wavefunction for these entered values
    '''

    s = np.copy(r)       # make copy of initial conditions so function can be called repeatedly
    psipoints = []       # array that will store the points for the wavefunction

    # loop over the x values
    for x in xpoints:
        psipoints += [s[0]]       # add initial confitions into psi points
        s += fourthOrderRungeKutta(schrodinger, s, x, h, E)    # solve the diff eq

    return np.array(psipoints, float)

# definition of various potentials
def Vinf(x):
    '''
        square well potenial

        input:
            x (float): value to evaluate potential at

        returns:
            value of potential for the given x value
    '''
    L = 1.0       # absolute value of the x-coordinate of the walls of the well

    if np.abs(x) < L:
        # if particle is located within the walls of the well, its potential is 0
        return 0.0

    else:
        # particle is located outside of the well
        return 100.0

def Vabs(x):
    '''
        potential that looks like absolute value function

        input:
            x (float): value to evaluate potential at

        returns:
            value of potential for the given x value
    '''

    return np.abs(x)

def Vsquared(x):
    '''
        potential that looks like x^2

        input:
            x (float): value to evaluate potential at

        returns:
            value of potential for the given x value
    '''

    return x**2

# main code block
# initialize values
V = Vsquared        # choose potential function to use
max = 3.0           # max value of x to go out to
h = 0.001           # spacing between the x values
targetAccuracy = 1e-6

# initials values of psi and phi at x = 0 stored in array, respectively
# for an even parity solution
r = np.array([1, 0], float)
print('Initial values for psi and phi, the derivative of psi:', r)

# x values to find wavefunction for
x = np.arange(0.0, max, h)

# i know that the energy eigenvalue is between these two numbers
E1 = 0.6
E2 = 0.8

# calculate the energy eigenvalue using the secant method
while np.abs(E1-E2) > targetAccuracy:
    # get the wavefunction for E1
    psipoints = waveFunction(r, schrodinger, x, h, E1)
    # get the wavefunction value at the boundary value
    psi1 = psipoints[-1]

    # get the same for E2
    psipoints = waveFunction(r, schrodinger, x, h, E2)
    psi2 = psipoints[-1]

    E1, E2 = E2, E2 - psi2*(E2-E1)/(psi2-psi1)

# E2 gives the value of the eigenenergy
energyEigenvalue = E2

print(f'The energy eigenvalue is {energyEigenvalue:.5f}')

# generate the wavefunction for this energy eigenvalues
psi = waveFunction(r, schrodinger, x, h, energyEigenvalue)

# extend wavefunction and range of x-values for negative values
psi = np.append(psi[::-1], psi[1:])
x = np.append(-x[::-1], [x[1:]])

# Normalize wavefunction
deltaX = h

print("<psi|psi>:", psi.dot(psi) * deltaX)
Norm = np.sqrt( psi.dot(psi) * deltaX )
print("Renormalizing by:", Norm)
psi = psi/Norm
print("<psi|psi>:",psi.dot(psi)*deltaX,"\n")

# Calculate expectation value <x^2>
print("<psi|x^2|psi>:", psi.dot( x*x*psi ) * deltaX,"\n")

# plot the normalized wavefunction
fig = plt.figure(1, figsize=(10,8))
plt.plot(x, psi, 'r.', color = '#7cb8a4')
plt.ylim(-0.1,1)     # need to put in something, in case the function explodes
plt.xlabel('x')
plt.ylabel(r'$\psi$')
plt.title('The Normalized Wavefunction of the Ground State\n for a x^2 Potential ')
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('partB_plot.png', format = 'png')        # saves figure
plt.show()
plt.clf()
