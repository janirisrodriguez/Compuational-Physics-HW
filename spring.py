#! /usr/bin/env python3

'''
spring.py is a python script that finds the equilibrium angle for a mass being suspended from two springs for given
parameters using the bisection method, the false position method, the Newton-Raphson method, and the secant method and
shows the different values that each methohd yields along with the rate of convergence for each one.

Janiris Rodriguez
PHZ 4151C
Mar 11, 2021
'''

import numpy as np
import sys

# defining necessary values for equation, all in SI units
m = 5.0       # mass of object
L_0 = 0.3     # half the distance between the two supports and spring rest length
k = 1000.0    # spring constant
g = 9.81      # acceleration due to gravity

def f(theta):
    '''
        the function to find the zeros of to find equilibrium angle for a mass hanging from two springs

        input:
            theta (float): the inside angle between the spring and the ceiling in degrees
        returns:
            the value of the function for a given angle
    '''
    # calculating a constant term here for the sake of readability
    term_denom = 2.0 * k * L_0
    term = m * g / term_denom

    # convert angle to radians because numpy trig function requires angle to be in radians
    theta = np.radians(theta)

    # combine all the terms
    y = np.tan(theta) - np.sin(theta) - term

    return y

def f_prime(theta):
    '''
        derivative of the function to find the zeros of to find equilibrium angle for a mass hanging from
        two springs

        input:
            theta (float): the inside angle between the spring and the ceiling in degrees
        returns:
            the value of the derivative for a given angle
    '''
    # convert angle to radians because numpy trig function requires angle to be in radians
    theta = np.radians(theta)

    # term that appears repeatedly in equation
    term = np.cos(theta)

    # combine terms
    y = (1.0 / term**2) - term

    return y

def binarySearch(x_1, x_2, epsilon, func):
    '''
        tries to find root of func in between two entered x values using the binary search method

        input:
            x_1 (float): point at which to start search for root
            x_2 (float): point at which to end search for root
            epsilon (float): accuracy to be reached, target distance between the x values
            func (function): function to find root of
        returns:
            either the position of x value if func(x_1) and func(x_2) have opposite signs and the number of
            iterations it took to reach the target accuracy as a list or an exit if not
    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached
    zero_Found = False


    # checking to make sure that f(x1) and f(x2) have opposite signs. if they do, this division will yield negative number
    # necessary for these two values to have opposite signs for binary search method to work
    if func(x_1)/func(x_2) < 0:

        # counter to track number of iterations it takes to reach the target accuracy
        counter = 0

        # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
        while not zero_Found:
            x_prime = (x_1 + x_2) / 2.0         # find midpoint between two values
            f_prime = func(x_prime)

            # check to see if this new x is the root
            if func(x_prime) == 0:
                zero_Found = True

            # check to see if value of function at new x value has same sign as function at either of the two points
            # if they do, replace that original x value with the new value
            elif f_prime/func(x_1) > 0:
                x_1 = x_prime
            else:
                x_2 = x_prime

            # calculates the distance between the two points to check if desired accuracy has been reached
            if abs(x_1 - x_2) <= epsilon:
                zero_Found = True

            counter += 1
        # after desiredAccuracy has been reached, calculate the midpoint the two x values one more time
        # this is the final estimate for where the zero of the function is
        zero = (x_1 + x_2) / 2.0

        # increment counter
        counter += 1

        # format result to return as a list of root and counter
        result = [zero, counter]

        return result

    # f(x1) and f(x2) start off with the same sign so it's not possible to use binary search to find zero
    else:
        sys.exit('f(x1) and f(x2) have the same sign initially. Binary search method failed.')

def falsePositionMethod(x_1, x_2, targetAccuracy, func):
    '''
        tries to find root of func in between two entered x values using the binary search method

        input:
            x_1 (float): point at which to start search for root
            x_2 (float): point at which to end search for root
            epsilon (float): accuracy to be reached, target distance between the x values
            func (function): function to find root of
        returns:
            either the position of x value if func(x_1) and func(x_2) have opposite signs and the number of
            iterations it took to reach the target accuracy as a list or an exit if not
    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached or if the function value is zero
    zero_Found = False

    # checking to make sure that f(x1) and f(x2) have opposite signs. if they do, this division will yield negative number
    # necessary for these two values to have opposite signs for binary search method to work
    if func(x_1)/func(x_2) < 0:

        # counter to track number of iterations it takes to reach the target accuracy
        counter = 0

        # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
        while not zero_Found:

            # calculate the slope
            slope_num = func(x_2) - func(x_1)
            slope_denom = x_2 - x_1
            slope = slope_num / slope_denom

            # calculate y-intercept
            y_intercept = func(x_1) - (slope * x_1)

            # calculate guess for root using slope and y-intercept
            x_prime = -y_intercept / slope

            # check to see if this new x is the root
            if func(x_prime) == 0:
                zero_Found = True

            # check to see if value of function at new x value has same sign as function at either of the two points
            # if they do, replace that original x value with the new value
            if func(x_prime)/func(x_1) > 0:
                x_1 = x_prime
            if func(x_prime)/func(x_2) > 0:
                x_2 = x_prime

            if counter > 0:
                # calculates the distance between the two points to check if desired accuracy has been reached
                if abs(x_prime - old_x_prime) <= targetAccuracy:
                    zero_Found = True

            # set current x_prime value to the old one for the next iteration of the loop to check for the accuracy
            old_x_prime = x_prime

            # increment counter
            counter += 1

        # format result to return as a list of root and counter
        result = [x_prime, counter]

        return result

    # f(x1) and f(x2) start off with the same sign so it's not possible to use false position to find zero
    else:
        sys.exit('f(x1) and f(x2) have the same sign initially. False position method failed.')

def newtonMethod(x_current, targetAccuracy, func, func_prime):
    '''
        finds the zero of a function using Newton's method

        input:
            x_current (float): starting point for Newton's method
            targetAccuracy (float): accuracy to be reached
            func (function): function to find root of
            func_prime (function): derivtaive of the function to find root of
        returns:
            location of the root of function to entered accuracy and the number of iterations it took to reach the
            target accuracy as a list

    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached
    zero_Found = False

    # counter to track number of iterations it takes to reach the target accuracy
    counter = 0

    # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
    while not zero_Found:

        # calculates guess for the location of the root
        term = func(x_current) / func_prime(x_current)
        x_prime = x_current - term

        # check to see if this new x is the root
        if func(x_prime) == 0:
            zero_Found = True

        # calculates the distance between the two points to check if desired accuracy has been reached
        if abs(x_prime - x_current) <= targetAccuracy:
            zero_Found = True

        # set variable to prepare for either for next iteration of loop or to return location of root if desired accuracy was reached
        x_current = x_prime

        # increment counter
        counter += 1

    # format result to return as a list of root and counter
    result = [x_current, counter]

    return result

def secantMethod(x_1, x_2, targetAccuracy, func):
    '''
        finds the zero of a function using the secant method

        input:
            x_1 (float): starting point for secant method
            x_2 (float): ending point for secant method
            targetAccuracy (float): accuracy to be reached
            func (function): function to find root of
        returns:
            location of the root of function to entered accuracy and the number of iterations it took to reach the
            target accuracy as a list
    '''
    # boolean variable to be used as condition for while loop. True when desired accuracy is reached
    zero_Found = False

    # counter to track number of iterations it takes to reach the target accuracy
    counter = 0

    # loop until desired accuracy is found, that will be when zero_Found is set to True and loop ends
    while not zero_Found:

        # find the slope between two points, necessary for calculation of new guess for root
        slope_num = func(x_2) - func(x_1)
        slope_denom = x_2 - x_1
        slope = slope_num / slope_denom

        # calculate new guess for location of root
        x_prime = x_2 - (func(x_2) / slope)

        # check to see if this new x is the root
        if func(x_prime) == 0:
            zero_Found = True
        # calculates the distance between the two points to check if desired accuracy has been reached
        if abs(x_prime - x_2) <= targetAccuracy:
            zero_Found = True

        # prepare variables for next iteration of loop assuming that the root has not been found yet
        x_1 = x_2
        x_2 = x_prime

        # increment counter
        counter += 1

    # format result to return as a list of root and counter
    result = [x_prime, counter]

    return result



# main code block

# values to search for equilibrium angle in between, we know that the angle must be in between these values or else the problem
# would not make physical sense, but these are also guesses that yield reasonable values
theta_start = 7.0
theta_end = 60.0

# precision to determine angle to
desiredAccuracy = 1.0e-3

binaryResult = binarySearch(theta_start, theta_end, desiredAccuracy, f)
falsePositionResult = falsePositionMethod(theta_start, theta_end, desiredAccuracy, f)
newtonResult = newtonMethod(theta_start, desiredAccuracy, f, f_prime)
secantResult = secantMethod(theta_start, theta_end, desiredAccuracy, f)

print(f'Using the bisection method, the equilibrium angle is {binaryResult[0]:.3f} degress and it took {binaryResult[1]} iterations.')
print(f'Using the false position method, the equilibrium angle is {falsePositionResult[0]:.3f} degress and it took {falsePositionResult[1]} iterations.')
print(f'Using the Newton-Raphston Method method, the equilibrium angle is {newtonResult[0]:.3f} degress and it took {newtonResult[1]} iterations.')
print(f'Using the secant method, the equilibrium angle is {secantResult[0]:.3f} degress and it took {secantResult[1]} iterations.')
