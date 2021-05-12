#! /usr/bin/env python3

'''
radioactiveDecay_varyingTau.py is a python script that calculates the number of radioactive nuclei at different times
using numerical differentiation via forward difference to solve the differential equation for radioactive nuclei
for varying mean lifetimes. It also plots the results found using the various tau values.

Janiris Rodriguez
PHZ 4151C
Feb 24, 2021
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

    time = []                # list containing values for the time that N is evaluated at, set by spacing
    timeValue = a            # counter that represents time that N is evaluated at

    time.append(timeValue)   # first element is starting time

    numPoints = int((b - a) / spacing)       # number of points necessary for the given spacing

    for i in range(numPoints - 1):

        # calculates N for the next time value
        nextTerm = const * N[i]
        N.append(nextTerm)

        # increment time counter
        timeValue += spacing

        # keeps track of the times that N is evaluated at
        time.append(timeValue)

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
    N = []   # list containing values for the number of radioactive nuclei for some time

    for i in range(len(time)):

        # calculate term in exponential
        temp_exponent = -time[i] / meanLifetime

        # calculate N for this given time value, time[i]
        temp_N = initialValue * np.exp(temp_exponent)
        N.append(temp_N)

    return N

# main code block
start = 0.0                         # lower bound for range of time value in s
stop = 15.0                         # lower bound for range of time value in s
tau = [5.0, 3.0, 1.0, 0.1, 0.01]    # mean lifetime in s
h = 0.01                            # time elapsed in s
initial = 100.                      # number of particles initially (sample is at 100%)]

numPoints = (stop - start) / h                          # calculates number of points are necessary for this given h
t = np.linspace(start, stop, int(numPoints)).tolist()   # list of times to find number of particles at, as a list

numParticles = []     # will store number of particles for each different tau, will contain 5 different lists

for i in range(len(tau)):
    # save list of number of particles for a given tau into a temporary list
    temp_numParticles = radioactiveDecay_forwardDifference(start, stop, h, initial, tau[i])[1]
    #append this list numParticles
    numParticles.append(temp_numParticles)


#plot number of particles as function of time
for i in range(len(tau)):
    plt.plot(t, numParticles[i], label = f'tau = {tau[i]} s')

plt.title(f'Number of Particles Throughout Radioactive Decay with h = {h} s')
plt.xlabel('Time (s)')
plt.ylabel('N (as a percentage)')
plt.legend()
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('radioactiveDecay_varyingTau_numVtime_plot.png')   # saves figure
plt.show()
plt.clf()
