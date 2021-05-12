'''
satelliteAltitude.py is a python script that takes in the period of a satellite's orbit above Earth and calculates
the necessary altitude it needs to be at above the Earth's surface. It also calculates the altitudes of satellites
with orbits of 24 hours, 23.93 hours (sidereal day) 90 minutes, and 45 minutes. Negative altitudes imply that the
orbit is not possible.

Janiris Rodriguez
PHZ 4151C
Jan 31, 2020
'''

import numpy as np

def calculateAltitude(time, G = 6.67e-11, M = 5.97e24, R = 6371e3):
    '''
        calculates the necessary altitude of an orbit when given the length of its orbit
        input:
            time (float): length of orbit in seconds
            G (float): gravitational constant in m^3 kg^-1 s^-2
            M (float): mass of Sun in kg
            R (float): radius of Earth in m
        returns:
            altitude of orbit
    '''
    h_1 = (G * M * time**2.) / (4 * (np.pi)**2.) # calculating terms separately to find h
    h = h_1**(1/3.) - R
    return h

#Part B

T = int(input('Enter in a value for T, length of a satellite\'s orbit in seconds, around Earth to find the altitude it must have, \nT:'))


print(f'\nAltitude above Earth: {calculateAltitude(T):.2e} m')

#Part C

t_1day = 24 * 3600
t_90min = 90 * 60
t_45min = 45 * 60

print(f'\n\nAltitude above Earth for an orbit every 24 hours: {calculateAltitude(t_1day):.2e} m')
print(f'Altitude above Earth for an orbit every 90 minutes: {calculateAltitude(t_90min):.2e} m')
print(f'Altitude above Earth for an orbit every 90 minutes: {calculateAltitude(t_45min): .2e} m')

#Part D
t_sidereal = 23 * 3600 + 60 * .93

difference = calculateAltitude(t_1day) - calculateAltitude(t_sidereal)

print(f'\nAltitude above Earth for a geosynchronous orbit: {calculateAltitude(t_sidereal):.2e}', 'm')
print(f'The difference in altitudes for a geosyncronous orbit and a 24 hour orbit is {difference:.2e} m')
