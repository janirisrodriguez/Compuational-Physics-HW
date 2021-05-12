#! /usr/bin/env python3

'''
lotkaVolterra.py is a python script that plots how the populations of foxes and rabbits evolve over time based on
the Lotka-Volterra model with given intial conditions. The differential equations in the model are solved using the
fourth order Runge-Kutta method.

Janiris Rodriguez
PHZ 4151C
Mar 19, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def f(r):
    '''
        represents the differential equations describing how the populations of rabbits and foxes evolve over time
        using the Lotka-Volterra model, all numbers are represented in thousands

        input:
            r (2d array of floats): first index represents number of rabbits, second index represents number of foxes
                                        both in thousands
        returns:
            2d array containing the change in the number of rabbits and foxes with respect to time, respectively

    '''
    # initializing constants used for rabbits and foxes
    alpha = 1.0
    beta = 0.5
    gamma = 0.5
    delta = 2.0

    # storing the number of rabbits and foxes sent in into different variables for readability
    x = r[0]     # number of rabbits
    y = r[1]     # number of foxes

    # stores the product of the nunmber of foxes and rabbits for readability
    product = x*y

    # calculate results of differential equations set by the model
    f_x = alpha * x - beta * product
    f_y = gamma * product - delta * y

    # store the results into a 2d array
    result = np.array([f_x, f_y])

    return result

# main code block
# initial conditions, initial number of rabbits and foxes (in thousands)
x_0 = 2.0
y_0 = 2.0

# initializing the time range to observe the behavior of the rabbits and foxes and the spacing required based on
# how many data points are collected
start = 0.0
stop = 30.0
numPoints = 1000
spacing = (stop - start) / numPoints

time = np.linspace(start, stop, numPoints)    # create array of times

x = np.zeros(numPoints)   # create array to store number of rabbits at each time step
y = np.zeros(numPoints)   # create array to store number of foxes at each time step

r = np.array([x_0, y_0])  # array meant to store the current number of rabbits and foxes, initialize it with inital conditions

# loop over how many time points we have
for i in range(numPoints):

    # store the number of rabbits and foxes into their respective arrays from r
    x[i] = r[0]
    y[i] = r[1]

    # implementation of the fourth order Runge-Kutta method
    k1 = spacing * f(r)
    k2 = spacing * f(r + 0.5*k1)
    k3 = spacing * f(r + 0.5*k2)
    k4 = spacing * f(r + k3)

    # storing the new values for the populations based on evaluation of the k's above and the previous population values
    r += (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0

# plot the number of animals in each population as a function of time
plt.plot(time, x, label = 'Rabbits', color = 'magenta')
plt.plot(time, y, label = 'Foxes', color = 'orange')
plt.xlabel('Time')
plt.ylabel('Number of Animals (in Thousands)')
plt.title('Population of Rabbits and Foxes using \nthe Lotka-Volterra Model')
plt.legend(edgecolor = 'white')          # creates legend
plt.xlim([start, stop])
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('lotkaVolterra.png')        # saves figure
plt.show()
plt.clf()
