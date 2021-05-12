#! /usr/bin/env python3

'''
quadraticEquations.py is a python script that calculates the roots of an entered quadratic equation two different
ways

Janiris Rodriguez
PHZ 4151C
Feb 3, 2021
'''

import numpy as np

def rootMethod1(a,b,c):

    sqrt_term = b**2 - 4 * a * c
    denom = 2 * a

    x_plus = (-b + np.sqrt(sqrt_term)) / denom
    x_minus = (-b - np.sqrt(sqrt_term)) / denom

    return x_minus, x_plus

def rootMethod2(a,b,c):

    sqrt_term = b**2 - 4 * a * c
    num = 2 * c

    x_plus = num / (-b + np.sqrt(sqrt_term))
    x_minus = num / (-b - np.sqrt(sqrt_term))

    return x_plus, x_minus

square = float(input('Constant in front of the squared term: '))
linear = float(input('Constant in front of the linear term: '))
const = float(input('Constant term: '))

root1_method1, root2_method1 = rootMethod1(square, linear, const)
root1_method2, root2_method2 = rootMethod2(square, linear, const)

print(f'The solutions to that quadratic equation via Method 1 are x = {root1_method1} and x = {root2_method1}')
print(f'The solutions to that quadratic equation via Method 2 are x = {root1_method2} and x = {root2_method2}')
