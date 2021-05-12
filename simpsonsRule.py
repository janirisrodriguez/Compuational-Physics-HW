#! /usr/bin/env python3

'''
simpsonsRule.py is a python script that calculates the result of an integral using Simpson's rule

Janiris Rodriguez
PHZ 4151C
Feb 8, 2021
'''

def f(x):
    '''
       defines the function to integrate
       input:
           x (float): dependent variable for funtion
        returns:
            value of function for a given x value, x^4 - 2x + 1
    '''
    y = x**4 - 2*x + 1
    return y


def simpsonsRule(a,b,N):
    '''
        calculates value of an integral using Simpson's rule
        input:
            a (float): lower limit of integral
            b (float): upper limit of integral
            N (int): number of slices
        returns:
            approximate value of integral
    '''
    h = (b - a)/ N    # spacing for fitting quadratics
    I = f(a) + f(b)   # starting term in sum to find result of integral

    for k in range(N):

        # sum over k in between 2 and N-2 for even k
        if k % 2 == 0 and k >= 2 and k <= (N-2):
            I += 2 * f(a + k*h)

        # sum over k in between 1 and N-1 for odd k
        if k % 2 == 1 and k >= 1 and k <= (N-1):
            I += 4 * f(a + k*h)

    I *= h/3

    return I


# main code block
slices = [10,100,1000]
start = 0
stop = 2
values = []

for i in range(len(slices)):
    # calculate value of integral of f(x) for a various number of slices
    temp = simpsonsRule(start,stop,slices[i])
    values.append(temp)
    print('The approximate value for the integral using Simpson\'s rule with', slices[i], f'slices is {values[int(i)]:.12f}')

# calculates fractional error - |result - 4.4| / 4.4
fractionalError = abs(values[0] - 4.4) / 4.4

print(f'The fractional error using {slices[0]} slices is {fractionalError:.3e}')
