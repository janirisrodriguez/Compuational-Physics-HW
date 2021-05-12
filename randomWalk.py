#! /usr/bin/env python3

'''
randomWalk.py is a python script that produces 5 random walks for a given number steps. It also saves these paths
as a graph to show the path visually.

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

# main code block
gridSize = 101          # size of lattice
stepNum = 2000          # number of steps taken by particle

# generate 5 random walks
for i in range(1,6):

    # name of file to save plot to
    fileName = 'randomWalk_iteration'  + str(int(i)) + '.png'

    # positions of particle throughout random walk
    X, Y = randomWalk(gridSize, stepNum)

    # plots the path of the particle
    for i in range(stepNum):
        plt.plot([X[i], X[i+1]], [Y[i], Y[i+1]], 'k-', lw = 0.5)

    plt.title(f'Random Walk for {stepNum} Steps - Iteration {i}')

    axes = plt.gca()

    # formatting the plot
    axes.set_xlim([0,gridSize-1])
    axes.set_ylim([0,gridSize-1])

    # saves the plot
    plt.savefig(fileName, format = 'png')
    plt.clf()
