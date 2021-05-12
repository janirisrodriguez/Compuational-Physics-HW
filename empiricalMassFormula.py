'''
empiricalMassFormula.py is a python script that calculates the nuclear binding energy of an atomic nucleus and 
thhe binding energy per nucleon when given the atomic number and mass number of an atom

Janiris Rodriguez
PHZ 4151C
Jan 31, 2020
'''

import numpy as np

def calculateBindingEnergy(mass_Num, atom_Num):
    a1 = 15.67
    a2 = 17.23
    a3 = 0.75
    a4 = 93.2

    if atom_Num % 2 == 0 and (atom_Num - mass_Num) % 2 == 0:
        a5 = 12.
    elif atom_Num % 2 == 1 and (atom_Num - mass_Num) % 2 == 1:
        a5 = -12.
    else:
        a5 = 0.

    term1 = a1 * mass_Num
    term2 = -a2 * mass_Num**(2/3)
    term3 = -a3 * atom_Num**2 / mass_Num**(1/3)
    term4 = -a4 * (mass_Num - 2 * atom_Num)**2 / mass_Num
    term5 = a5 / mass_Num**(1/2)

    bindingEnergy = term1 + term2 + term3 + term4 + term5

    return bindingEnergy

A = int(input('Mass number: '))
Z = int(input('Atomic number: '))

B = calculateBindingEnergy(A, Z)
B_perNucleon = B/A

print(f'The binding energy for this atom is {B:.2f} MeV')
print (f'The binding energy per nucleon for this atom is {B_perNucleon:.2f} MeV')
