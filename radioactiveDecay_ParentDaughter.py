#! /usr/bin/env python3

'''
radioactiveDecay_ParentDaughter.py is a python script that calculates the number of parent and daughter radioactive
nuclei at different times using numerical differentiation via forward difference to solve the differential equation
for radioactive nuclei for varying mean lifetimes for the daughter nuclei. It also plots the results found using the
various tau values.

Janiris Rodriguez
PHZ 4151C
Feb 24, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def radioactiveDecay_parent(time, spacing, initialValue, meanLifetime):
    '''
        calculates values for the number of parent radioactive nuclei as they decay at some time, equation for this
        found using the forward difference method to define the derivative of N numerically and plugging that into the
        differential equation for the parent decaying nuclei.

        inputs:
            time (list of floats): list of the times that the number of radioactive nuclei will be evaluated at
            spacing (float): step that time value is incrementing by
            initialValue (float): how much of the parent radioactive nuclei is present represented as a percentage
                                    (initalValue = 100 means that the whole sample is present initally,
                                    initalValue = 50 means that half is, etc.)
            meanLifetime (float): the mean lifetime of the parent nuclei, (dimensions of meanLifetime must be given
                                    by [meanLifetime] = [time])

        returns:
            list of the number of parent radioactive nuclei at the given time values
    '''

    N = []                      # list containing values for the number of parent radioactive nuclei for some time
    N.append(initialValue)      # first element is the number of parent nuclei initially present

    const = 1.0 - (spacing / meanLifetime)   # constant present in calculating N, for the sake of readability

    for i in range(len(time) - 1):
        # calculates N for the next time value
        nextTerm = const * N[i]
        N.append(nextTerm)

    return N

def radioactiveDecay_daughter(time, spacing, initialValue, meanLifetime, N_parent, meanLifetime_parent):
    '''
        calculates values for the number of daughter radioactive nuclei as they decay at some time, equation for this
        found using the forward difference method to define the derivative of N numerically and plugging that into
        the differential equation for the daughter decaying nuclei.

        inputs:
            time (list of floats): list of the times that the number of daughter radioactive nuclei will be
                                     evaluated at
            spacing (float): step that time value is incrementing by for
            initialValue (float): how much of the daughter radioactive nuclei is present represented as a percentage
                                    (initalValue = 100 means that the whole sample is present initally,
                                    initalValue = 50 means that half is, etc.)
            meanLifetime (float): the mean lifetime of daughter nuclei, (dimensions of meanLifetime must be given
                                    by [meanLifetime] = [time])
            N_parent (list of floats): the number of parent nuclei at the given time values
            meanLifetime_parent (float): the mean lifetime of parent nuclei

        returns:
            list of the number of daughter radioactive nuclei at the given time values
    '''

    N = []                    # list containing values for the number of daughter radioactive nuclei for some time
    N.append(initialValue)    # first element is the number of nuclei initially present of the daughter nuclei

    const = 1.0 - (spacing / meanLifetime)         # constant present in calculating N, for the sake of readability
    const_parent = spacing / meanLifetime_parent   # constant present in front of parent term when calculating N

    for i in range(len(time)-1):
        # calculates the two terms necessary to find N for the next value of N
        term_parent = const_parent * N_parent[i]
        term_daughter = const * N[i]

        # combine these two to find N and append this value to the list
        temp_N = term_parent + term_daughter
        N.append(temp_N)

    return N

# main code block
start = 0.0                     # lower bound for range of time value in s
stop = 15.0                     # lower bound for range of time value in s
tau_P = 2.0                     # mean lifetime in s for the parent nuclei
tau_D = [0.02, 2.0, 200.0]      # mean lifetime in s for the daughter nuclei
h = 0.001                       # time elapsed in s
initial_P = 100.0               # number of parent particles initially (sample is at 100%)
initial_D = 0.0                 # number of daughter particles initially (no daughter particles are present)

numPoints = (stop - start) / h                          # calculates number of points are necessary for this given h
t = np.linspace(start, stop, int(numPoints)).tolist()   # list of times to find number of particles at, as a list

N_P = []         # will store number of parent particles
N_D = []         # will store number of daughter particles for each value of tau_D, will contain 3 different lists

# finds the number of parent particles for the given time range
N_P = radioactiveDecay_parent(t, h, initial_P, tau_P)

# finds the number of the daughter particles for the given time range for the varying taus
for i in range(len(tau_D)):
    temp_N = radioactiveDecay_daughter(t, h, initial_D, tau_D[i], N_P, tau_P)
    N_D.append(temp_N)

#plot number of particles as function of time
plt.plot(t, N_P, label = f'number of parent particles for tau = {tau_P}')
for i in range(len(tau_D)):
    plt.plot(t, N_D[i], label = f'number of daughter particles for tau = {tau_D[i]} s')
plt.title(f'Number of Particles Throughout Parent and Daughter Nuclei Radioactive Decay with h = {h} s')
plt.xlabel('Time (s)')
plt.ylabel('N (as a percentage)')
plt.legend()
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('radioactiveDecay_ParentDaughter_numVtime_plot.png')   # saves figure
plt.show()
plt.clf()
