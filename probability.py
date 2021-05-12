#! /usr/bin/env python3

#FINISH THIHS PROGRAM

'''
probability.py is a python script that calculates the probability of a coin toss landing on heads a certain number
of times

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

    coeff = 1

    if k!= 0:

        for i in range(n):
            if (n-i) > (n-k):
                coeff *= (n-i)
            if (i+1) <= k:
                coeff /= (i+1)

    return int(coeff)

def probability(n,k):
    '''
        calculates the probability of heads landing k times in n coin tosses
        input:
            n (int): number of coin tosses
            k (int): number of times heads lands
        returns:
            probability of heads landing k times in n coin tosses
    '''

    prob_Num = binomial(n,k)
    prob_Denom = 2**n
    prob = prob_Num / prob_Denom

    return prob

# main code block
timesFlipped = int(input('Enter how many times a coin will be flipped: '))
heads = int(input('Enter how many times heads will land: '))

heads_Probability = probability(timesFlipped, heads)

print(f'The probability of getting heads {heads} time(s) when a coin is flipped {timesFlipped} time(s) is ', heads_Probability)
