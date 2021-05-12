#! /usr/bin/env python3

'''
hypersphere.py is a python script that can find the volume of an n-dimensional hypersphere using the Monte Carlo
mean-value method to approximate the value of the integral (specifically found for 0-12 dimensions) and plots the
volume as a function of dimension. Also finds the error using different number of sample points for a 10-d
hypersphere and plots this error as a function of number of sample points.

Janiris Rodriguez
PHZ 4151C
Feb 21, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def withinSphere(arg, dim):
    '''
        evaluates whether given point is within a {dim}-dimenional sphere
        input:
            arguement (list of floats): represents point to evaluate
            dim (int): number of elements in arguements, represents number of dimensions for sphere
        returns:
            1 if the point (arguement) is within the sphere, 0 if it isn't
    '''

    # value will store the result of the sum of the arguements squared to check if it would be inside the {dim}-dimensional sphere
    value = 0

    for i in range(dim):
        value += (arg[i]**2)

    # checks to see if this point is within the sphere, it is within the sphere if it less than or equal to 1
    # if it is, result of function is 1, if not, it is 0
    if value <= 1:
        result = 1
    else:
        result = 0

    return result


def montecarloIntegration(func, dim, lim, N):
    '''
        based on textbook function for the Monte Carlo mean-value integration method of any dimension
        input:
            func (function): user-defined function to be integrated over, takes in a list as an arguement
            dim (int): number of dimensions being integrated over
            lim (2-d list of floats): stores limits of integration for dim dimensions. first index represents the dimension,
                                      second index represents either the lower limit (element 0) or upper limit (element 1) of integration
            N (int): number of sample points
        returns:
            result of integral and a list of lists of random values used as arguements for the function
    '''
    I = 1.0 / N      # stores value of integral, starts by storing 1/N, which helps set up finding average of function
    summation = 0    # stores value of summation for N random arguemnts sent to function to find average value of function
    argList = []     # stores lists of random values used as arguements for the function

    # multiplies inetgral value by the subtraction of lower limit of integral from upper limit of integral for the ith dimension
    for i in range(dim):
        I *= (lim[i][1] - lim[i][0])

    for i in range(N):
        # stores arguements to send to function for one iteration (ie sample point)
        arg = []

        # generating dim number of random arguements within the bounds of integration for the jth dimension
        # to send to function being integrated
        for j in range(dim):
            arg.append(np.random.uniform(lim[j][0], lim[j][1]))

        # adds the result of function with these randomly produced arguements
        summation += func(arg, dim)

        #stores this iteration's line up of random numbers to find error
        argList.append(arg)

    # multiplies result of sum into value of integral
    I *= summation

    return I, argList

def errorMonteCarlo(func, arg, dim, lim, N):
    '''
        find the error on the integral when using the Monte Carlo mean-value method
        input:
            func (function): user-defined function to be integrated over, takes in a list as an arguement
            arg (2-d list): stores arguements used to find value of integral using the montecarloIntegration function. first index
                                represents which sample point out of N is being evaluated, the second index represents a specific
                                coordinate value for that sample point
            dim (int): number of dimensions being integrated over
            lim (2-d list): stores limits of integration for dim dimensions. first index represents the dimension,
                                      second index represents either the lower limit (element 0) or upper limit (element 1) of integration
            N (int): number of sample points
        returns:
            error on the integral estimation
    '''

    var_term1 = 1. / N          # will store the expectation value of func^2 to find variance of func
    var_term2 = 1. / (N**2)     # will store the expectation value squared of func to find variance of func
    summation1 = 0              # will store sum of func values for given arg values to calculate 1st term of variance of func
    summation2 = 0.             # will store sum of func values for given arg values to calculate 2nd term of variance of func
    sigma = 1. / np.sqrt(N)     # will store error

    # multiplies error value by the subtraction of lower limit of integral from upper limit of integral for the ith dimension
    for j in range(dim):
        sigma *= (lim[j][1] - lim[j][0])

    # finds values of function for a given arguement to add to summations for the terms in thhe variance of func
    for i in range(int(N)):
        val = func(arg[j], dim)
        summation1 += val ** 2
        summation2 += val

    # multiply in the respective summations to find the two terms of the variance
    var_term1 *= summation1
    var_term2 *= summation2

    # combine the two variance terms and take square root to find the error on func
    sigma *= np.sqrt(var_term1 - var_term2)

    return sigma


# main code block
numPoints = 1000000               # number of sampling points for integration
numDimension = 10                 # number of dimensions hypersphere is
limit = [-1,1]                    # bounds of integration, -1 to 1 for all dimensions

limit_10d = []                    # list containing limits of integration for 10 dimensions
arguements_10d = []               # list containing arguements used for the integration in dimensions

# limits of integration for all 10 dimensions are -1 to 1
for i in range(numDimension):
    limit_10d.append(limit)

# calculate volume of 10-d hypersphere
volume_10d, arguements_10d = montecarloIntegration(withinSphere, numDimension, limit_10d, numPoints)

print(f'The volume of a 10-d hypersphere is {volume_10d}\n')

lowerDim = 0
upperDim = 12
dimensionRange = [*range(lowerDim, upperDim)]  # range of dimensions from 0 to 12
volumes = []                                   # store volumes of spheres for given dimensions in dimensionRange
arguments = []                                 # stores arguements used to calculate the volume of spheres for given dimensions

for i in dimensionRange:
    # creating a temporary list of limits for each iteration
    limit_list = []
    # appends appropriate number of limits for a given dimension to send into Monte Carlo function
    for j in range(len(dimensionRange)):
        limit_list.append(limit)
    # find volumes for each dimension in dimensionRange
    # saves these to temporary variables to then append to their respective lists
    tempVolume, tempArg = montecarloIntegration(withinSphere, dimensionRange[i], limit_list, numPoints)
    volumes.append(tempVolume)
    arguments.append(tempArg)

    print(f'The (hyper)volume of a {i}-d sphere is approximately {volumes[i]:.4f}')


#graph of hypervolume v. dimension
plt.plot(dimensionRange, volumes)
plt.xlabel('Dimension')
plt.ylabel('Hypervolume')
plt.title('Hypervolume v. Number of Dimension')
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('dimension_hypervolume_plot.png')   # saves figure
plt.show()
plt.clf()

lowerNumPoints = 20000                              # bottom of range for number of sampling points
step = 20000                                        # step between different point values
number = int((numPoints - lowerNumPoints) / step)   # calculates how many different numbers of sample points there should be for given step value

# generates sample point range from {lowerNumPoints} to {numPoints} in steps of {step} as a list
numPointsRange = np.linspace(lowerNumPoints, numPoints, number).tolist()

errors_10d = []             # stores the errors in the estimation of integral for 10-d hypersphere

print('\nFor a 10-d hypersphere, the error on the volume is:')

counter = 0     # for the purpose of printing out errors

for i in numPointsRange:
    # find error in integral result for 10-d hypersphere for i sample points
    errors_10d.append(errorMonteCarlo(withinSphere, arguements_10d, numDimension, limit_10d, i))
    print(f'{errors_10d[int(counter)]} for {i} steps')
    counter += 1

#graph of error v. sample points
plt.plot(numPointsRange, errors_10d)
plt.xlabel('Number of Sample Points')
plt.ylabel('Error on Volume')
plt.title('Error on Volume of 10-d Hypershpere v. N')
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('error_N_plot.png')   # saves figure
plt.show()
plt.clf()
