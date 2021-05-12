#! /usr/bin/env python3

'''
limit_1.py is a python script that calculates the derivative of a function using the limit definition of the
derivative with delta = 10^-2
ways

Janiris Rodriguez
PHZ 4151C
Feb 3, 2021
'''

def f(x):
    y = x * (x-1)
    return y

def limit(d):
    num = f(1 + d) - f(1)
    lim = num / d
    return lim

delta = 1e-2
derivative = limit(delta)

print(f'Using the limit definition of the derivative of x(x-1) at x=1 when the limit approaches {delta} is {derivative}')
