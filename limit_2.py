#! /usr/bin/env python3

'''
limit_2.py is a python script that calculates the derivative of a function using the limit definition of the
derivative with various deltas
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

derivativeList = []
delList = []
delList.append(1e-4)

for i in range(5):
    delList.append(delList[i] * 1e-2)

for i in range(len(delList)):
    derivativeList.append(limit(delList[i]))
    print(f'Using the limit definition of the derivative of x(x-1) at x=1 when the limit approaches {delList[i]} is {derivativeList[i]}')
