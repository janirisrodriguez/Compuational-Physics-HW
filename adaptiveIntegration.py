#! /usr/bin/env python3

'''
adaptiveIntegration.py is a python script that evaluates an integral for a given function using 2 methods of
adaptive integration: adaptive trapezoidal rule and adaptive Simpson's rule. It also shows many slices it takes for
each method to obtain a desired accuracy and compares the two methods.

Janiris Rodriguez
PHZ 4151C
Feb 9, 2021
'''

import numpy as np

def f(x):
    '''
       defines the function to integrate
       input:
            x (float): dependent variable for funtion
        returns:
            value of function for a given x value, (sin(sqrt(100x)))^2
    '''
    arg = np.sqrt(100*x)
    y = np.sin(arg) ** 2
    return y

def adaptiveTrapezoidalRule(a, b, desiredAccuracy):
    '''
        calculates value of an integral using the adaptive trapezoidal rule method
        input:
            a (float): lower limit of integral
            b (float): upper limit of integral
            desiredAccuracy (float): approximate accuracy desired for value of integral
        returns:
            nothing
    '''
    # starting with one slice
    N = 1
    # result of trapezoidal rule for 1 slice, initializing the first term for adaptive integration method
    I_current = 0.5*f(a) + 0.5*f(b)

    print('Adaptive trapezoidal rule:')

    # imitates do-while loop, breaks out of loop when desired accuracy is achieved
    while True:

        if N != 1:

            # defining spacing for certain slice number
            h_current = (b - a) / N
            # making sure that this term starts at 0 for summation for new number of slices
            sum_current = 0.

            # sum over k from 1 to N-1 for odd k, adding terms necessary
            for k in range(1,N,2):
                sum_current += f(a + k*h_current)

            # result of integral for this given slice number
            I_current = 0.5*I_prev + h_current*sum_current
            # calculating the approximate accuracy
            epsilon_current = (I_current - I_prev) / 3.


            print(f'{N} slice(s): the estimate of the integral is {I_current:.6f} and the estimate of the error of the integral is {epsilon_current}')

            # checks for whether desired accuracy has been achieved
            if abs(epsilon_current) <= abs(desiredAccuracy):
                break

        # increments slice and establishes variables for next iteration of loop with different slice number
        N *= 2
        I_prev = I_current

    return

def adaptiveSimpsonsRule(a, b, desiredAccuracy):
    '''
        calculates value of an integral using the adaptive Simpson's rule method
        input:
            a (float): lower limit of integral
            b (float): upper limit of integral
            desiredAccuracy (float): approximate accuracy desired for value of integral
        returns:
            nothing
    '''
    # starting with 1 slice
    N = 1
    # initializing S,T, and the result of the integral, I, for 1 slice
    S_current = (f(a) + f(b)) / 3.
    T_current = 0
    I_current = (b - a) * S_current

    print('\n\nAdaptive Simpson\'s rule:')

    # imitates do-while loop, breaks out of loop when desired accuracy is achieved
    while True:

        if N != 1:

            # defining spacing for certain slice number
            h_current = (b - a) / N
            # making sure that this term starts at 0 for summation for new number of slices
            T_current = 0

            # sum over k from 1 to N-1 for odd k, adding terms necessary
            for k in range(1,N,2):
                T_current += f(a + k*h_current)

            # finalizing terms for result of integral for certain slice number
            T_current *= 2/3.
            S_current = S_prev + T_prev
            # result of integral for certain slice number
            I_current = h_current * (S_current + 2*T_current)
            # calculating the approximate accuracy
            epsilon_current = (I_current - I_prev) / 15.

            print(f'{N} slice(s): the estimate of the integral is {I_current:.6f} and the estimate of the error of the integral is {epsilon_current}')

            # checks for whether desired accuracy has been achieved
            if abs(epsilon_current) <= abs(desiredAccuracy):
                break

        # increments step and establishes variables for next iteration of loop with different slice number
        N *= 2
        T_prev = T_current
        S_prev = S_current
        I_prev = I_current

    return

# main code block
# evaluating integral to an accuracy of 10^(-6)
adaptiveTrapezoidalRule(0,1,1e-6)
adaptiveSimpsonsRule(0,1,1e-6)
