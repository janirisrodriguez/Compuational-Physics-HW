#! /usr/bin/env python3

'''
brownianMotion.py is a python script that uses Brownian motion to find the average distance squared and
root-mean-square distance for a given number of particles (1000) for some lattice size (10001) and number of steps
(100000) whose mean free path is 1cm.

Janiris Rodriguez
PHZ 4151C
Feb 21, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def randomWalk(L, N):
    '''
       generates a random path for a particle
       input:
           L (int): size of one side of grid to make an LxL grid
           N (int): number of steps in random walk
        returns:
            two lists, one containing information about the particle's motion in x and the other containing
            information about the particle's motion in y
    '''

    # keeps track of where particle has been
    locationHistory_X = []
    locationHistory_Y = []

    # places particle at center of grid
    current_X = int((L-1) / 2)
    current_Y = int((L-1) / 2)
    locationHistory_X.append(current_X)
    locationHistory_Y.append(current_Y)

    # keeps track of current step number
    counter = 0

    # loops until the particle has made N moves
    while counter < N:

        #1 is up, 2 is right, 3 is down, 4 is left
        futureStep = np.random.randint(1,5)

        # if the future step is out of bounds, starts loop over again, avoids counting this situation as a step
        if futureStep == 1 and current_Y == L-1:
            continue
        if futureStep == 3 and current_Y == 0:
            continue
        if futureStep == 2 and current_X == L-1:
            continue
        if futureStep == 4 and current_X == 0:
            continue

        # if we are here, the future move for the particle is in bounds. this moves particle to new location
        if futureStep == 1:
            current_Y += 1
        elif futureStep == 3:
            current_Y -= 1
        elif futureStep == 2:
            current_X += 1
        else:
            current_X -= 1

        # save this new location to the lists
        locationHistory_X.append(current_X)
        locationHistory_Y.append(current_Y)

        # increments the step number
        counter+=1

    return locationHistory_X, locationHistory_Y

def calculateDistance(x_0, y_0, x_f, y_f):
    '''
       calculates distance between two points
       input:
           x_0 (float): initial x position
           y_0 (float): initial y position
           x_f (float): final x position
           y_f (float): final y position
        returns:
            the distance between (x_0, y_0) and (x_f, y_f)
    '''

    xTerm = (x_f - x_0) ** 2
    yTerm = (y_f - y_0) ** 2

    # distance between two points
    d = np.sqrt(xTerm + yTerm)

    return d

# main code block
gridSize = 10001          # size of lattice
stepNum = 100000          # number of steps taken by particle
particleNum = 1000        # number of particles we calculate path for
l = 1.                    # mean free path

# stores distances and distances squared between inital and final points in random walk in cm and cm^2, respectively
distance = []
distanceSquared = []

for i in range(particleNum):
    # positions of particle throughout random walk
    X, Y = randomWalk(gridSize, stepNum)

    # calculate distance and distance squared for above random walk
    distance.append(calculateDistance(X[0], Y[0], X[-1], Y[-1]))
    distanceSquared.append(distance[i]**2)

# find average distance squared. cast variables into floats to avoid integer math
avg_distanceSquared = float(sum(distanceSquared)) / float(len(distanceSquared))

# finds the root-mean-square distance in cm
distance_rms = np.sqrt(stepNum)*l

print(f'The average distance squared is {avg_distanceSquared:.4f} cm^2')
print(f'The root-mean-square distance is {distance_rms:.4f} cm')
