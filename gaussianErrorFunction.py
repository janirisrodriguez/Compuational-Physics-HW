#! /usr/bin/env python3

'''
gaussianErrorFunction.py is a python script that calculates the Gaussian Error Function for a given range of x
values using trapezoidal rule and plots this Gaussian Error Function

Janiris Rodriguez
PHZ 4151C
Feb 8, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

def f(t):
    '''
       defines the function to integrate
       input:
           t (float): dependent variable for funtion
        returns:
            value of function for a given t value, e^(-x^2)
    '''
    y = np.exp(-t**2)
    return y

def trapezoidalRule(a,b,N):
    '''
        calculates value of an integral using trapezoidal rule
        input:
            a (float): lower limit of integral
            b (float): upper limit of integral
            N (int): number of slices
        returns:
            approximate value of integral
    '''
    h = (b - a) / N          # spacing for fitting the straight line segments
    I = 0.5*f(a) + 0.5*f(b)  # starting term in sum to find result of integral

    for k in range(1, N):
        # sums over k from 1 to N-1
        I += f(a + k*h)

    I *= h

    return I


# main code block
start = 0
stop = 3
stepSize = 0.1
N = 1000
E = []           # values of Gaussian error function that will be stored as list


num = int((stop - start) / stepSize)    # number of values that will be stored for E(x)
x = np.linspace(start, stop, num)       # numpy array of {num} evenly spaced x values in between {start} and {stop}


for i in range(len(x)):
    E.append(trapezoidalRule(x[0], x[i], N))    # calculating values of E using trapezoidal rule

# converting list to numpy array
E = np.array(E)

# plotting the Gaussian error function as a function of x
plt.plot(x, E, color = 'black')
plt.xlabel('x')
plt.ylabel('E')
plt.title('Gaussian Error Function')
ax = plt.gca()                                  # gets the axes for this specific plot
ax.spines['top'].set_visible(False)             # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('gaussianErrorFunction_plot.png')   # saves figure
plt.show()
plt.close()
