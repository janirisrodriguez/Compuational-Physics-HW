#! /usr/bin/env python3

'''
duffingOscillator.py is a python script that solves the differential equation for Duffing's oscillator by creating
two first-order differential equations from one second-order differential equation and solving those differential
equation using the fourth-order Runge-Kutta method for various values for the parameters of B and b. Then plots x v.
time and the phase space for each case case.

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

# storing the values for the various test cases into a list
B_list = np.array([7.0, 7.0, 10.0, 7.0])       # damping coefficient multiplied by 2, in 1/s
b_list = np.array([6.0, 0.6, 0.05, 0.01])      # amplitude of the driving force divided by mass in m

# initializing the time range to get data points for and the spacing required based on how many data points are collected
numPoints = 10000
numPeriods = 25      # the number of periods we want to record data for
start = 0.0
stop = numPeriods * 2 * np.pi / omega_d    # calculate ending time value based on angular frequency of driving force and how many periods we want to show
time = np.linspace(start, stop, numPoints) # create array of times
spacing = (stop - start) / numPoints

# initialize 2d arrays for x and v to store the values of the oscillations for each test case
x_list = np.zeros((len(B_list), numPoints))
v_list = np.zeros((len(B_list), numPoints))

# array to temporarily hold 1 iteration in 1 test case
# initial values are the same for all test cases
r = np.array([x_0, v_0])

# loop over how many test cases there are
for i in range(len(B_list)):
    # create 2 temporary lists to store x and v values for the ith test case
    x = np.zeros(numPoints)
    v = np.zeros(numPoints)

    # loop over the number of data points to be collected
    for j in range(numPoints):
        # store the  values into their respective arrays from r
        x[j] = r[0]
        v[j] = r[1]

        # implementation of the fourth order Runge-Kutta method
        k1 = spacing * f(r, time[j], b_list[i], B_list[i])
        k2 = spacing * f(r + 0.5*k1, time[j] + 0.5*spacing, b_list[i], B_list[i])
        k3 = spacing * f(r + 0.5*k2, time[j] + 0.5*spacing, b_list[i], B_list[i])
        k4 = spacing * f(r + k3, time[j] + spacing, b_list[i], B_list[i])

        # storing the new values for the populations based on evaluation of the k's above and the previous x and v values
        r += (k1 + 2.0*k2 + 2.0*k3 + k4) / 6.0

    # after one iteration of the Runge-Kutta method for a given test case, store these x and v arrays into another arrays
    x_list[i] = x
    v_list[i] = v

# loop over the number of test cases
for i in range(len(b_list)):
    # plot the y coordinate as a function of time
    plt.plot(time, x_list[i], color = '#84B9C4')
    plt.xlabel('Time (s)')
    plt.ylabel('x (m)')
    plt.title(f'x vs. Time for Duffing\'s Oscillator \nfor B={B_list[i]} m and b={b_list[i]} 1/s')
    plt.xlim([start, stop])
    ax = plt.gca()                           # gets the axes for this specific plot
    ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
    ax.spines['right'].set_visible(False)
    plt.savefig(f'3b.x_timePlot_{i+1}.png')        # saves figure
    plt.show()
    plt.clf()

    # plot the phhase space
    plt.plot(x_list[i], v_list[i], color = '#B0CA72')
    plt.xlabel('x (m)')
    plt.ylabel('v (m/s)')
    plt.title(f'Phase Space for Duffing\'s Oscillator \nfor B={B_list[i]} m and b={b_list[i]} 1/s')
    ax = plt.gca()                           # gets the axes for this specific plot
    ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
    ax.spines['right'].set_visible(False)
    plt.savefig(f'3b.phaseSpace_Plot_{i+1}.png')        # saves figure
    plt.show()
    plt.clf()
