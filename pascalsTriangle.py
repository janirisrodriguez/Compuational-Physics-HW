#! /usr/bin/env python3
'''
pascalsTriangle.py is a python script that prints out the first 20 lines of Pascal's triangle


Janiris Rodriguez
PHZ 4151C
Feb 3, 2021
'''

def binomial(n,k):

    '''
        calculates the binomial coefficient for given n and k
        input:
            n (int): represents binomial power - (1+x)^n
            k (int): represents the power of x in the expansion
        returns:
            binomial coefficient of x^k of (1+x)^n
    '''

    # initialize coefficient, also handles when k=0
    coeff = 1

    if k!= 0:

        for i in range(n):
            # (n-i) represents one term of (n-k)! for numerator
            if (n-i) > (n-k):
                coeff *= (n-i)
            # (i+1) represents one term of k! for denominator
            if (i+1) <= k:
                coeff /= (i+1)

    return int(coeff)

def pascalTriangle(line):

    '''
        prints Pascal's triangle
        input:
            line(int): prints this number of lines of Pascal's triangle
        returns:
            nothing
    '''

    for i in range(line):
        for j in range(i+1):

            # for formatting purposes, keeps all terms of the same line of Pascal's triangle in the same line
            if i!=j:
                print(binomial(i,j), end =' ')
            else:
                print(binomial(i,j))
    return

# main code block - prints 20th line of Pascal triangle

pascalTriangle(20)
