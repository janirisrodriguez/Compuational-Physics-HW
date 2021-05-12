'''
planetaryOrbits.py is a python script that takes in the distance and velocity of an object at its perihelion and
calculates various properties of its orbits. Also prints information about the orbits of Earth and Halley's Comet

Janiris Rodriguez
PHZ 4151C
Jan 31, 2020
'''

import numpy as np

M = 1.9891e30
G = 6.6738e-11

def calculate_Aph(l_per, v_per, M = 1.9891e30, G = 6.6738e-11):

    k = 2. * G * M / l_per

    b = -k / v_per
    c = -(v_per**2 - k)

    v_aph = (-b - np.sqrt(b**2 - 4*c)) / 2.

    l_aph = l_per * v_per / v_aph

    return l_aph, v_aph


def orbitQualities(l_p, l_a, v_p):

    semiMajor = (l_p + l_a) / 2.
    semiMinor = np.sqrt(l_p * l_a)

    period_Num = 2. * np.pi * semiMajor * semiMinor
    period_Denom = l_p * v_p
    period = period_Num / period_Denom
    period = period / (3600 * 24 * 365)

    ecc_Num = l_a - l_p
    ecc_Denom = l_a + l_p
    eccentricity = ecc_Num / ecc_Denom

    return period, eccentricity


l1 = float(input('Enter the distance to the Sun at the perihelion in m: '))
v1 = float(input('Enter the velocity at the perihelion in m/s: '))

l2, v2 = calculate_Aph(l1, v1)
T, ecc = orbitQualities(l1, l2, v1)

print(f'\n\nThe distance from the Sun at the aphelion is {l2:.4e} m')
print(f'The velocity at the aphelion is {v2:.4e} m/s')
print(f'The period of the orbit is {T:.4e} yr')
print(f'The eccentricity of the orbit is {ecc:.4e}')

l1_earth = 1.4710e11
v1_earth = 3.0287e4

l2_earth, v2_earth = calculate_Aph(l1_earth, v1_earth)
T_earth, ecc_earth = orbitQualities(l1_earth, l2_earth, v1_earth)

print(f'\n\nThe distance of Earth from the Sun at its aphelion is {l2_earth:.4e} m')
print(f'The velocity of Earth at its aphelion is {v2_earth:.4e} m/s')
print(f'The period of Earth\'s orbit is {T_earth:.4e} yr')
print(f'The eccentricity of Earth\'s orbit is {ecc_earth:.4e}')

l1_halley = 8.7830e10
v1_halley = 5.4529e4

l2_halley, v2_halley = calculate_Aph(l1_halley, v1_halley)
T_halley, ecc_halley = orbitQualities(l1_halley, l2_halley, v1_halley)

print(f'\n\nThe distance of Halley\'s comet from the Sun at its aphelion is {l2_halley:.4e} m')
print(f'The velocity of Halley\'s comet at its aphelion is {v2_halley:.4e} m/s')
print(f'The period of Halley\'s comet\'s orbit is {T_halley:.4e} yr')
print(f'The eccentricity of Halley\'s comet\'s orbit is {ecc_halley:.4e}')
