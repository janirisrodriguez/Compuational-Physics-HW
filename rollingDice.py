#! /usr/bin/env python3

'''
rollingDice.py is a python script that simulates the rolling of two dice for a given amount of rolls and calculates
the number of times that a double six is rolled, fraction of times one gets a double six, and prints out the dice
values thrown up to and including the first double six, the number of double sixes rolled, the number of dice
throws, the double six fraction, and the average number of throws between double six combinations.

Janiris Rodriguez
PHZ 4151C
Feb 22, 2021
'''

import numpy as np

def twoDice():
    '''
       generates 2 random numbers in between 1 and 6 to simulate two dice being rolled
       input:
            none
        returns:
            two numbers representing the values of the dice thrown
    '''

    # two random integers generated between. and 6
    roll1 = np.random.randint(1,7)
    roll2 = np.random.randint(1,7)

    return roll1, roll2

num_rolls = 1000000           # number of rolls performed
num_doubleSix = 0.            # stores how many double six rolls there are
num_betweenDoubSix = 0        # stores how many rolls there are in between double six rolls for one instance
num_betweenDoubSixList = []   # list that stores how many rolls there are in between double six rolls for all iterations
stopPrint = False             # boolean variable that dictates when to stop printing, will stop when set to True

# rolls dice num_rolls times
for i in range(num_rolls):

    # two dice are rolled
    roll_one, roll_two = twoDice()

    # prints values of dice with iteration number as long as stopPrint is False (ie up until first double six)
    if not stopPrint:
        print(f'Roll {i+1}: {roll_one}, {roll_two}')

    # double six is rolled
    if roll_one == 6 and roll_two == 6:
        # increments variable storing how many double sixes are rolled
        num_doubleSix += 1
        # adds num_betweenDoubSix to list to keep track of how many rolls there are in b/w double six rolls
        num_betweenDoubSixList.append(num_betweenDoubSix)
        # resets num_betweenDoubSix to 0 because a double six was rolled
        num_betweenDoubSix = 0
        # sets stopPrint to True to prevent future print statements
        stopPrint = True

    else:
        # if anything other than double six is rolled, then variable storing how many rolls there are in between
        # double six rolls is incremented
        num_betweenDoubSix += 1

# calculates double six fraction
fraction_DoubleSix = num_doubleSix / num_rolls

# calculates average number of throws in between double six rolls
avg_betweenDoubSix = sum(num_betweenDoubSixList) / float(len(num_betweenDoubSixList))

print(f'\n\nNumber of double sixes: {int(num_doubleSix)}')
print(f'Number of dice rolls: {num_rolls}')
print(f'Double six fraction: {fraction_DoubleSix:.4f}')
print(f'Average number of throws in between double six combinations: {int(avg_betweenDoubSix)}')
