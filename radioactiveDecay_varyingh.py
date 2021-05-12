#! /usr/bin/env python3

'''
radioactiveDecay_varyingh.py is a python script that calculates the number of radioactive nuclei at different times
using numerical differentiation via forward difference to solve the differential equation for radioactive nuclei
for varying values of h. It also plots the results found using the various h values against the analytical solution
and plots the fractional error when using the different h values.

Janiris Rodriguez
PHZ 4151C
Feb 23, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def radioactiveDecay_forwardDifference(a, b, spacing, initialValue, meanLifetime):
    '''
        calculates values for the number of radioactive nuclei as they decay at some time, equation for this found
        using the forward difference method to define the derivative of N numerically and plugging that into the
        differential equation for decaying nuclei.

        inputs:
            a (float): lower bound for range of time values
            b (float): upper bound for range of time values
            spacing (float): step that time value is incrementing by
            initialValue (float): how much of the radioactive nuclei is present represented as a percentage
                                    (initalValue = 100 means that the whole sample is present initally,
                                    initalValue = 50 means that half is, etc.)
            meanLifetime (float): the mean lifetime of the given nuclei, (dimensions of meanLifetime must be given
                                    by [meanLifetime] = [a])

        returns:
            list of the times that the number of radioactive nuclei was evaluated at (set by spacing) and the list
            of the number of radioactive nuclei at those time values


    '''

    N = []                            # list containing values for the number of radioactive nuclei for some time
    N.append(initialValue)            # first element is the number of nuclei initially present

    const = 1.0 - (spacing / meanLifetime)   # constant present in calculating N, for the sake of readability

    iteration = 0            # counter meant to keep track of how many times loop has iterated

    time = []                # list containing values for the time that N is evaluated at, set by spacing
    timeValue = a            # counter that represents time that N is evaluated at

    # loop until maximum time in range has been reached
    while timeValue < b:

        # keeps track of the times that N is evaluated at
        time.append(timeValue)

        # calculates N for the next time value
        nextTerm = const * N[iteration]
        N.append(nextTerm)

        # increment both counters
        iteration += 1
        timeValue += spacing

    # need to add final time at the end of the list
    time.append(b)

    return time, N

def radioactiveDecay_analytical(time, initialValue, meanLifetime):
    '''
        calculates values for the number of radioactive nuclei as they decay at some time, equation for this found
        by solving the differential equation that describes this system analytically.

        inputs:
            time (list of floats): list of the times that the number of radioactive nuclei will be evaluated at
            initialValue (float): how much of the radioactive nuclei is present represented as percentage
                                    (initalValue = 100 means that the whole sample is present initally,
                                    initalValue = 50 means that half is, etc.)
            meanLifetime (float): the mean lifetime of the given nuclei, (dimensions of meanLifetime must be given
                                    by [meanLifetime] = [a])

        returns:
            list of the number of radioactive nuclei at the given time values


    '''
    N = []      # list containing values for the number of radioactive nuclei for some time

    for i in range(len(time)):

        # calculate term in exponential
        temp_exponent = -time[i] / meanLifetime

        # calculate N for this given time value, time[i]
        temp_N = initialValue * np.exp(temp_exponent)
        N.append(temp_N)

    return N

# main code block
start = 0.0                 # lower bound for range of time value in s
stop = 15.0                 # lower bound for range of time value in s
tau = 2.0                   # mean lifetime in s
initial = 100.              # number of particles initially (sample is at 100%)
h = [1.0, 0.1, 0.01]        # time elapsed in s

numPoints = 100000         # number of points that the analytical eqn for the radioactive decay will be evaluated at
time_analytical = np.linspace(start, stop, numPoints).tolist()  # times that analytical eqn for the radioactive decay will be evaluated at

numberParticles = []   # will store number of particles for each time interval, will contain 4 different lists
                       # will contain 4 different lists (3 for the different h values and 1 for the analytical)
time = []              # will store time intervals for each time interval, will contain 4 different lists (for same reason as above)

for i in range(len(h)):

    # find the different time and N values for a given h and store these in temporary variables
    temp_time, temp_N = radioactiveDecay_forwardDifference(start, stop, h[i], initial, tau)

    # append these temporary variables to the appropriate lists
    time.append(temp_time)
    numberParticles.append(temp_N)

# include analytical case to the time and numberParticle lists
time.append(time_analytical)
numberParticles.append(radioactiveDecay_analytical(time[-1], initial, tau))

fractionalError = []      # will store fractional error values as a 2d list

# calculating fractional error for the different h values
for i in range(len(h)):
    # will store the fractional error values for 1 h value
    tempError = []

    # calculates the actual number of particles for the given times used in this specific instance of h
    analyticalComparison = radioactiveDecay_analytical(time[i], initial, tau)

    for j in range(len(time[i])):
        # calculating fractional error for each N term and appending onto temporary list
        num = abs(numberParticles[i][j] - analyticalComparison[j])
        tempError.append(num / analyticalComparison[j])
    # after all the fractional errors for that specific h value are put into temporary list, append that list to fractional error list
    fractionalError.append(tempError)

#plot number of particles as function of time
for i in range(len(time)):
    plt.plot(time[i], numberParticles[i])

plt.xlabel('Time (s)')
plt.ylabel('N (as a percentage)')
plt.title(f'Number of Particles Throughout Radioactive Decay for tau = {tau} s')
plt.legend([f'forward difference with h = {h[0]}',f'forward difference with h = {h[1]}', f'forward difference with h = {h[2]}', 'analytical'])
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('radioactiveDecay_varyingh_numVtime_plot.png')   # saves figure
plt.show()
plt.clf()

#plot fractional as function of time
for i in range(len(fractionalError)):
    plt.plot(time[i], fractionalError[i])

plt.xlabel('Time (s)')
plt.ylabel('Fractional Error')
plt.title(f' Fractional Error in Number of Particles Throughout Radioactive Decay for tau = {tau} s')
plt.legend([f'forward difference with h = {h[0]}',f'forward difference with h = {h[1]}', f'forward difference with h = {h[2]}'])
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('radioactiveDecay_varyingh_errorVtime_plot.png')   # saves figure
plt.show()
plt.clf()
