#! /usr/bin/env python3

'''
primeNumbers.py is a python script that finds prime numbers up to a given number by checking if each number in the range
from 3 to that given number by checking if each number is divisible by an of the primes in the primes list up to and
including the square root of the number being checked. It also prints out this list of prime numbers.

Janiris Rodriguez
PHZ 4151C
Mar 1, 2021
'''

import numpy as np

def isPrime(num, listPrimes):
    '''
       evaluates whether the given number is prime
       input:
            num (int): number being evaluated
            listPrimes (list of ints): list of prime numbers
        returns:
            a boolean statement, returns True if num is prime and False if not
    '''
    prime = True       # set variable to True, every number is prime until proven to not be

    # loop over list of prime numbers
    for i in range(len(listPrimes)):
        # only need to evaluate the prime numbers in the list that are less than the square root of number being evaluated
        if listPrimes[i] <= int(np.sqrt(num)):
            # if the number being evaluated is divisible by any of these prime numbers, then it is not prime
            if num % listPrimes[i] == 0:
                prime = False
        # break out of loop if the prime numbers in the list are greater than the square root of number being evaluated
        else:
            break
        # break out of loop if the number has already been found to not be a prime number
        if not prime:
            break

    return prime

# main code block
maximum = 10000       # number to generate list of prime numbers up until and including
prime_list = [2]      # start list of prime numbers, the first number is always 2

# loop over numbers from 3 up to and including the entered maximum number
for n in range(3, maximum + 1):
    # send to the function to evaluate whether n is prime, if it returns True, then n is prime and added to list
    if isPrime(n, prime_list):
        prime_list.append(n)

print(f'Prime numbers up to {maximum}:\n{prime_list}')
