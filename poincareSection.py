#! /usr/bin/env python3

'''
poincareSection.py is a python script that solves the differential equation for Duffing's oscillator by creating
two first-order differential equations from one second-order differential equation and solving those differential
equation using the fourth-order Runge-Kutta method for B = 7 and b = 0.01. Then plots the Poincare' section for the
given parameters.

Janiris Rodriguez
PHZ 4151C
Mar 20, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

# initializing constants to describe this oscillator
A = 1.0        # spring constant divided by mass in 1/(m*s)^(-2)
omega_d = 1.0  # angular frequency of driving force

def f(r, t, b, B):
    '''
        represents the motion of a short string as a set of 2 first-order differential equations where v = dx/dt

        input:
            r (2d array of floats): first index represents x in m, second index represents v in m/s
            t (float): time value in s
            b (float): damping coefficient divided by mass, in 1/s
            B (float): amplitude of the driving force divided by mass in m
        returns:
            2d array of floats of the change in x and v with respect to time, respectively

    '''

    # storing the values sent in into different variables for readability
    x = r[0]
    v = r[1]

    # calculate differential equations for x and v
    f_x = v
    f_v = B*np.cos(t * omega_d) - b*v - A * x**3

    # store the results into an array
    result = np.array([f_x, f_v])

    return result


# main code block
# initial conditions
x_0 = 3.0
v_0 = 0.0

# storing the values for the test case
B = 7.0      # damping coefficient divided by mass, in 1/s
b = 0.01     # amplitude of the driving force divided by mass in m

# initializing the time range to get data points for and the spacing required based on how many data points are collected
numPoints = 200000                           # the number of periods we want to record data for
start = 0.0
stop = 2000*np.pi
time = np.linspace(start, stop, numPoints)   # create array of times
spacing = (stop - start) / numPoints         # find spacing
stepsPoincare = int(2*np.pi / spacing)       # the interval between points to get time steps of 2*pi, used for plotting

# initialize array for x and v to store the values of the oscillations
x = np.zeros(numPoints)
v = np.zeros(numPoints)

# stores initial values
r = np.array([x_0, v_0])

# loop over the number of data points to be collected
for i in range(numPoints):
    # store the  values into their respective arrays from r
    x[i] = r[0]
    v[i] = r[1]

    # implementation of the fourth order Runge-Kutta method
    k1 = spacing * f(r, time[i], b, B)
    k2 = spacing * f(r + 0.5*k1, time[i] + 0.5*spacing, b, B)
    k3 = spacing * f(r + 0.5*k2, time[i] + 0.5*spacing, b, B)
    k4 = spacing * f(r + k3, time[i] + spacing, b, B)

    # storing the new values for the populations based on evaluation of the k's above and the previous x and v values
    r += (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0

# plot Poincare' section
plt.plot(x[::stepsPoincare], v[::stepsPoincare], '.', color = '#BF7365')
plt.xlabel('x (m)')
plt.ylabel('v (m/s)')
plt.title(f'Poincare\' Section for Duffing\'s Oscillator \nfor B={B} m and b={b} 1/s')
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig(f'poincare.png')        # saves figure
plt.show()
plt.clf()
