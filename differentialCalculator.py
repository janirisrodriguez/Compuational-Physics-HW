#! /usr/bin/env python3

'''
differentialCalculator.py is a python script that numerically calculates the derivative of a user-defined function.
It features a class, DifferentialCalculator, for which objects of this type can be differentiated using the central
difference method for any h. It plots this numerical derivative against the analytical derivative for a specified
range.

Janiris Rodriguez
PHZ 4151C
Feb 22, 2021
'''

import numpy as np
import matplotlib.pyplot as plt

class DifferentialCalculator:
    '''
        Objects of this type have two properties, the user-defined function and the interval at which the derivative
        is being evaluated at.

        Only has one function:
            __call__: for when the object is called
    '''
    def __init__(self, function, h = 1.0e-8):
        self.func = function
        self.h = h

    # what occurs when differentialCalculator object is called
    def __call__(self, x):
        '''
            finds the derivative of object's own function using the central difference method evaluated at x

            input:
                self (differentialCalculator): the object itself
                x (float): number at whihch the derivate is being evaluated at

            returns:
                result of derivative
        '''
        # calculating terms necessary for central difference for the sake of easier reading
        halfterm = self.h / 2.
        term1 = self.func(x + halfterm)
        term2 = self.func(x - halfterm)

        # combining the terms to find the derivative
        der = (term1 - term2) / self.h

        return der

def f(x):
    '''
       defines the function to differentiate

       input:
           x (float): dependent variable for funtion

        returns:
            value of function for a given x value
    '''

    trigTerm = np.tanh(2.0 * x)
    y = 1 + (0.5 * trigTerm)

    return y

def derivative_f(x):
    '''
       defines the analytical derivative of the f function from above, which is (sech(2x))^2

       input:
           x (float): dependent variable for funtion
           
        returns:
            value of derivative of function for a given x value
    '''

    trigterm = np.cosh(2.0 * x)
    y = 1.0 / (trigterm ** 2)

    return y

x = np.linspace(-2, 2, 1000)               # numpy array of 1000 numbers from -2 to 2

derivative = DifferentialCalculator(f)     # DifferentialCalculator object that will help find derivative of f

f_analyticalDerivative = np.zeros(len(x))  # will store terms from analytical derivative
f_numericalDerivative = np.zeros(len(x))   # will store terms from numerical derivative

for i in range(len(x)):
    # find analytical derivative of f using function declared above for given x values
    f_analyticalDerivative[i] = derivative_f(x[i])
    # calling derivative (DifferentialCalculator object) to find the numerical derivative for given x values
    f_numericalDerivative[i] = derivative(x[i])

# plot the two derivatives
plt.plot(x, f_numericalDerivative, label = 'Numerical Derivative')
plt.plot(x, f_analyticalDerivative, label = 'Analytical Derivative')
plt.title('Derivative of f Found Using Different Methods')
plt.xlabel('x')
plt.ylabel('f \'(x)')
plt.legend(edgecolor = 'white')
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('derivativeF_plot.png')      # saves figure
plt.show()
plt.clf()
