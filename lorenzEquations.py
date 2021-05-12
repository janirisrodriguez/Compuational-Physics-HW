#! /usr/bin/env python3

'''
lorenzEquations.py is a python script that solves the Lorenz equations using the fourth order Runge-Kutta method for
a given set of inital conditions. It also creates a plot of y vs. time and z vs. x.

Janiris Rodriguez
PHZ 4151C
Mar 20, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def f(coordinates):
    '''
        represents the Lorenz equations

        input:
            coordinates (3d array of floats): first index represents the x coordinate, second index represents y,
                third represents z
        returns:
            3d array containing the change in each of the different coordinates with respect to time, respectively

    '''

    # initializing constants used in the different equations
    sigma = 10.0
    r = 28.0
    b = 8.0/3.0

    # storing the coordinates into their respective variables for readability
    x = coordinates[0]
    y = coordinates[1]
    z = coordinates[2]

    # calculate results of differential equations
    f_x = sigma * (y - x)
    f_y = r*x - y - x*z
    f_z = x*y - b*z

    # store the results into an array
    result = np.array([f_x, f_y, f_z])

    return result

# main code block
# initial coordinate values
x_0 = 0.0
y_0 = 1.0
z_0 = 0.0

# initializing the time range to get data points for and the spacing required based on how many data points are collected
start = 0.0
stop = 50.0
numPoints = 10000
spacing = (stop - start) / numPoints

time = np.linspace(start, stop, numPoints)    # create array of times

x = np.zeros(numPoints)   # create array to store x values at each time step
y = np.zeros(numPoints)   # create array to store y values at each time step
z = np.zeros(numPoints)   # create array to store z values at each time step

r = np.array([x_0, y_0, z_0])  # array meant to store the current coordinate values, initialize it with inital conditions

# loop over how many time points we have
for i in range(numPoints):

    # store the coordinate values into their respective arrays from r
    x[i] = r[0]
    y[i] = r[1]
    z[i] = r[2]

    # implementation of the fourth order Runge-Kutta method
    k1 = spacing * f(r)
    k2 = spacing * f(r + 0.5*k1)
    k3 = spacing * f(r + 0.5*k2)
    k4 = spacing * f(r + k3)

    # storing the new values for the populations based on evaluation of the k's above and the previous coordinate values
    r += (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0

# plot the y coordinate as a function of time
plt.plot(time, y, color = '#A5B5D9')
plt.xlabel('Time')
plt.ylabel('y')
plt.title('y vs. Time From Lorenz Equations')
plt.xlim([start, stop])
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('y_LorenzPlot.png')        # saves figure
plt.show()
plt.clf()

# plot the z coordinate against the x coordinate
plt.plot(x, z, color = '#C38CB9')
plt.xlabel('x')
plt.ylabel('z')
plt.title('x vs. z From Lorenz Equations')
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('xz_LorenzPlot.png')        # saves figure
plt.show()
plt.clf()
