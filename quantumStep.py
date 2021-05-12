'''
quantumStep.py is a python script that calculates the transmission and reflection probabilities through
a one dimensional potential step for a particle of some energy

Janiris Rodriguez
PHZ 4151C
Jan 31, 2020
'''

import numpy as np

hbar = 1.055e-34
eV_to_joule = 1.6022e-19

E_i = 10 * eV_to_joule
V = 9 * eV_to_joule
m = 9.11e-31

c = np.sqrt(2 * m) / hbar

k_1 = c * np.sqrt(E_i)
k_2 = c * np.sqrt(E_i - V)

T = (4 * k_1 * k_2) / (k_1 + k_2)**2
R = ((k_1 - k_2) / (k_1 + k_2))**2

print('The transmission probability is ', T)
print('The reflection probability is ', R)
