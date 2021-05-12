#! /usr/bin/env python3

'''
gamma.py is a python script that plots the integrand of the gamma function for various values and finds the value
of the gamma function for various a values using adaptive Simpson's rule for the numerical integration method.

FIX DESCRIPTION

Janiris Rodriguez
PHZ 4151C
Feb 26, 2021
'''

import numpy as np
import matplotlib.pyplot as plt
import integration

def f(x, a):

    '''
       defines the function to integrate

       input:
           x (float): integration variable for funtion
           a (float): dependent variable for function

        returns:
            value of function for given x and a values
    '''
    y = x ** (a-1)
    y*= np.exp(-x)

    return y

def f_z(z, a):

    '''
       defines the function, f(x,a), to integrate as a function of z where z = x / (a - 1 + x)

       input:
           z (float): integration variable for funtion
           a (float): dependent variable for function

        returns:
            value of function for given z and a values
    '''

    # if statements in case the variable, a, is sent in as a tuple as a result of being an optional arguement
    if (type(a) is tuple):
        c = float(a[0]) - 1.0           # term that repeatedly shows up, writing as one variable for readability, a is tuple

    else:
        c = a - 1.0

    # constructing the term that appears repeatedly for readability
    # if statements in case the variable, z, is sent in as a list
    if (type(z) is list):
        term_num = c * z[0]
        term_denom = 1.0 - z[0]

    else:
        term_num = c * z
        term_denom = 1.0 - z
    term = term_num / term_denom

    # term in the exponential
    if (type(z) is list):
        exponent = c * np.log(term) - term
    else:
        exponent = c * np.log(term) - term

    # combining all the terms for the integrand
    # if statements in case the variable, z, is sent in as a list
    y = c * np.exp(exponent)
    if (type(z) is list):
        y /= (1.0 - z[0])**2
    else:
        y /= (1.0 - z)**2

    return y

def gamma(a):

    '''
       defines the gamma function, performs integral using the Monte Carlo mean-value method

       input:
           a (float): dependent variable for function

        returns:
            approximate value for integral
    '''

    lower = 0.0
    upper = 0.9999      # not integrating all the way to 1 because it leads to a divide by 0 error

    # integrate the integrand as a function of z (f_z), using adaptive Simpson's rule
    I = integration.adaptiveSimpsonsRule(f_z, lower, upper, 1e-5, a)

    return I

# main code block
x = np.linspace(0,5,100)  # range of x values from 0 to 5 for plotting

# these will store result of function for x (from above) and a (number after underscore sets the a value, ie y_2 has a=2)
y_2 = np.zeros(len(x))
y_3 = np.zeros(len(x))
y_4 = np.zeros(len(x))

for i in range(len(x)):
    # calculates value of function
    y_2[i] = f(x[i],2)
    y_3[i] = f(x[i],3)
    y_4[i] = f(x[i],4)

# plotting the integrand for varying a values as a function of x
plt.plot(x, y_2, label = 'a = 2')
plt.plot(x, y_3, label = 'a = 3')
plt.plot(x, y_4, label = 'a = 4')
plt.xlabel('x')
plt.ylabel('f = $x^{a-1}e^{-x}$')
plt.title('f v. x for Various "a" Values')
plt.legend(edgecolor = 'white')          # creates legend
ax = plt.gca()                           # gets the axes for this specific plot
ax.spines['top'].set_visible(False)      # gets rid of top and right axes (purely for aesthetics)
ax.spines['right'].set_visible(False)
plt.savefig('gamma_fvx_plot.png')        # saves figure
plt.show()
plt.clf()

# shows various values for gamma for a given a value
print(f'Gamma when a=3/2 is {gamma(1.5):.3f}')
print(f'Gamma when a=3 is {gamma(3.0):.5f}')
print(f'Gamma when a=6 is {gamma(6.0):.5f}')
print(f'Gamma when a=10 is {gamma(10.0):.5f}')
