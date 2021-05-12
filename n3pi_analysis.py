#! /usr/bin/env python3

'''
n3pi_analysis.py is a python script that analyzes the reaction
    g p -> n pi+ pi- pi+
it finds the invariant mass of the recoil neutron and various invariant masses based on a combination of particles and makes histograms of these

Created by Sean Dobbs, Addendum by Janiris Rodriguez
PHZ 4151C
Apr 7, 2021
'''

# Example 1:  old style text file parsing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Convert data from genr8 .dat format to a csv format, for pandas
input_file_name = "n3pi.dat"
output_file_name = "n3pi.csv"

# other variables
num_events_to_print = 3
num_events = 0     # keep track of of the number of events for debugging purposes

## format of one event
## 4   # number of particles
## 1 0 0.000000e+00 0.000000e+00 5.000000e+00 5.000000e+00    # ID charge px py pz E
## 8 1 -2.261780e-01 -1.984560e-01 1.946048e+00 1.974144e+00
## 9 -1 -7.765000e-02 7.233300e-02 1.372624e+00 1.383820e+00
## 8 1 5.548030e-01 -3.011580e-01 1.301439e+00 1.453219e+00


# open input and output files - the files will be automatically closed when we get out of the "with" statement
print("Converting %s to %s ..."%(input_file_name,output_file_name))
with open(input_file_name) as inf:
    with open(output_file_name, "w") as outf:
        # add header to define column names (output format) for pandas
        header  = "photon_pid photon_charge photon_px photon_py photon_pz photon_pe"
        header += " pip1_pid pip1_charge pip1_px pip1_py pip1_pz pip1_e"
        header += " pip2_pid pip2_charge pip2_px pip2_py pip2_pz pip2_e"
        header += " pim_pid pim_charge pim_px pim_py pim_pz pim_e"      # gotta add that newline
        outf.write(header)
        # dummy variables we use to save the information temporarily
        photon = []
        pip1 = []
        pip2 = []
        pim = []
        # to parse the file, we use our knowledge that we're looking at a reaction
        #  with 4 final state particles this part should be reworked for a different reaction
        #  note that there's no error checking, which is a bad practice... if there's a problem,
        #  hopefully an exception will be thrown...
        for line in inf:
            word = line.split()    # split line into a list of words (separated by whitespace)
            value = int(word[0])   # look at the first value on a line to decide what to do

            if value == 4:         # we're reading in 4 particles per event, so we know that each event starts with this
                num_pi_plus = 0
                # once we get to a new event, write the old one out
                outstr = " ".join(photon) + " " + " ".join(pip1) + " " +  " ".join(pip2) + " " +  " ".join(pim)
                if num_events <= num_events_to_print:
                    print ("write out: %s"%outstr)
                outf.write(outstr+'\n')
                num_events += 1

            elif value == 1:       # incoming beam photon
                if num_events <= num_events_to_print:
                    print("\tPhoton Beam with Energy: %f"%(float(word[5]) ) )
                # lazily parse the particle into a simple list
                photon = word[:6]    # finite bounds as a sanity check

            elif value == 8:       # pi+ meson
                if num_events <= num_events_to_print:
                    print("\tPiPlus[%d] meson with Energy: %f"%(num_pi_plus, float(word[5])) )
                num_pi_plus += 1
                if num_pi_plus == 1:
                    pip1 = word[:6]
                else:
                    pip2 = word[:6]

            elif value == 9:       # pi- meson
                if num_events <= num_events_to_print:
                    print("\tPiMinus meson with Energy: %f"%(float(word[5])) )
                pim = word[:6]

        # assume there's one more event left over
        outstr = " ".join(photon) + " " + " ".join(pip1) + " " +  " ".join(pip2) + " " +  " ".join(pim)
        outf.write(outstr+'\n')


# print some summary info
print("Converted %d Events"%num_events)

# how to read data in
csv_data_file = "n3pi.csv"

data = pd.read_csv(csv_data_file, delimiter = ' ')
data.head()

"""
# Example 2:  do more data manipulation in pandas
#import pandas as pd
#import numpy as np
# Convert data from genr8 .dat format to a csv format, for pandas
input_file_name = "n3pi.dat"
output_file_name = "n3pi.csv"
# Define structure of the dataframe:
df_dict = {}
particle_id = []
particle_charge = []
particle_mult_index = []
particle_px = []
particle_py = []
particle_pz = []
particle_e = []
# other variables
num_events_to_print = 3
num_events = 0     # keep track of of the number of events for debugging purposes
#Check particle multiplicities:
pip_mult_counter = 0
pim_mult_counter = 0
g_mult_counter = 0
#format of one event
#4   # number of particles
#1 0 0.000000e+00 0.000000e+00 5.000000e+00 5.000000e+00    # ID charge px py pz E
#8 1 -2.261780e-01 -1.984560e-01 1.946048e+00 1.974144e+00
#9 -1 -7.765000e-02 7.233300e-02 1.372624e+00 1.383820e+00
#8 1 5.548030e-01 -3.011580e-01 1.301439e+00 1.453219e+00
# open input and output files - the files will be automatically closed when we get out of the "with" statement
print("Converting %s to a DataFrame ..."%(input_file_name))
with open(input_file_name) as inf:
        for line in inf:
            word = line.split()    # split line into a list of words (separated by whitespace)
            value = int(word[0])   # look at the first value on a line to decide what to do
            # ignore the line, if value == 4:
            if value != 4:
                particle_id.append(value)
                particle_charge.append(int(word[1]))
                particle_px.append(float(word[2]))
                particle_py.append(float(word[3]))
                particle_pz.append(float(word[4]))
                particle_e.append(float(word[5]))
                # We might have multiple particles of the same kind:
                if value == 9:
                    particle_mult_index.append(pim_mult_counter)
                    pim_mult_counter += 1
                elif value == 1:
                    particle_mult_index.append(g_mult_counter)
                    g_mult_counter += 1
                elif value == 8:
                    particle_mult_index.append(pip_mult_counter)
                    pip_mult_counter += 1
            else:
                # Reset the multiplicity counters:
                pip_mult_counter = 0
                pim_mult_counter = 0
                g_mult_counter = 0

# Convert data collected data to the pandas pd:
df_dict['particle_id'] = particle_id
df_dict['particle_charge'] = particle_charge
df_dict['particle_mult_index'] = particle_mult_index
df_dict['particle_px'] = particle_px
df_dict['particle_py'] = particle_py
df_dict['particle_pz'] = particle_pz
df_dict['particle_e'] = particle_e
#This is a dataframe that simply contains all particle information
unsorted_df = pd.DataFrame(df_dict)
num_events = unsorted_df.shape[0] / 4.0 # Divide by 4, because we have four particles per event

# print some summary info
print("Converted %d Events"%num_events)
# Check the dataframe:
unsorted_df.head(10)
# We are not happy with the current dataframe format --> wish to list the particles individually:
photons = unsorted_df[unsorted_df['particle_id'] == 1].values   # return a numpy array of the rows with particle_id==1
first_piplus = unsorted_df[(unsorted_df['particle_id'] == 8) & (unsorted_df['particle_mult_index'] == 0)].values
second_piplus = unsorted_df[(unsorted_df['particle_id'] == 8) & (unsorted_df['particle_mult_index'] == 1)].values
piminus = unsorted_df[unsorted_df['particle_id'] == 9].values
sorted_df_columns = [
    'photon_pid',
    'photon_charge',
    'photon_px',
    'photon_py',
    'photon_pz',
    'photon_pe',
    'pip1_pid',
    'pip1_charge',
    'pip1_px',
    'pip1_py',
    'pip1_pz',
    'pip1_e',
    'pip2_pid',
    'pip2_charge',
    'pip2_px',
    'pip2_py',
    'pip2_pz',
    'pip2_e',
    'pim_pid',
    'pim_charge',
    'pim_px',
    'pim_py',
    'pim_pz',
    'pim_e',
]
# Now just combine all particles to one array and remove the column with the multiplicity information:
particle_collection = np.concatenate([
    np.delete(photons,1,1), # First index defines the row / column we wish to remove and the second index defines if we are dealing with a row / column
    np.delete(first_piplus,1,1),
    np.delete(second_piplus,1,1),
    np.delete(piminus,1,1)
],axis=1)
# Now convert the array to a dataframe
data = pd.DataFrame(particle_collection,columns=sorted_df_columns)
# Write the dataframe to a .csv-file:
data.to_csv(output_file_name,index=False) # Do not store the column index
data.head(10)
"""

# other examples
# DataFrame.info() gives some summary info
data.info()

# add some columns to the tree corresponding to invariant masses
def calc_invariant_mass(px, py, pz, e):
    return np.sqrt( e**2 - px**2 - py**2 - pz**2 )

data['mpi1'] = calc_invariant_mass(data['pip1_px'], data['pip1_py'], data['pip1_pz'], data['pip1_e'])
data['mpippip'] = calc_invariant_mass(data['pip1_px']+data['pip2_px'], data['pip1_py']+data['pip2_py'], data['pip1_pz']+data['pip2_pz'], data['pip1_e']+data['pip2_e'])
data['mpip1pim'] = calc_invariant_mass(data['pip1_px']+data['pim_px'], data['pip1_py']+data['pim_py'], data['pip1_pz']+data['pim_pz'], data['pip1_e']+data['pim_e'])

# do the same for other masses
data[ ['mpi1', 'mpippip', 'mpip1pim'] ].head(20)

# make some plots
ax = data["mpippip"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("M(pi1+pi2+) GeV")
ax.set_ylabel("Counts / 20 MeV")
plt.savefig('mpippip.png')

plt.clf()
# make some more plots
ax = data["mpip1pim"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("M(pi1+pim) GeV")
ax.set_ylabel("Counts / 20 MeV")
plt.savefig('mpip1pim.png')

# this is where I started adding code for the homework assignment

# need to add columns to represent the target proton and recoil neutron into the data frame because they are not in the
# original file, but we need the target information to calculate information about the neutron and it makes sense
# to include all this information in the data frame, even if the info about the target might be redundant since it starts
# at rest. will be in the same format as all the other particles with the exception of the particle id, because that is not
# particularly relevant to us

data['proton_charge'] = 1.0
data['proton_px'] = 0.0
data['proton_py'] = 0.0
data['proton_pz'] = 0.0
data['proton_e'] = 0.938
data['m_proton'] = calc_invariant_mass(data['proton_px'], data['proton_py'], data['proton_pz'], data['proton_e'])

# initialize all the neutron measurements by using finding the "missing" momentum
data['neutron_charge'] = 0.0
data['neutron_px'] = data['photon_px'] + data['proton_px'] - (data['pip1_px'] + data['pip2_px'] + data['pim_px'])
data['neutron_py'] = data['photon_py'] + data['proton_py'] - (data['pip1_py'] + data['pip2_py'] + data['pim_py'])
data['neutron_pz'] = data['photon_pz'] + data['proton_pz'] - (data['pip1_pz'] + data['pip2_pz'] + data['pim_pz'])
data['neutron_e'] = data['photon_pe'] + data['proton_e'] - (data['pip1_e'] + data['pip2_e'] + data['pim_e'])

# calculate the invariant mass of the neutron
data['m_neutron'] = calc_invariant_mass(data['neutron_px'], data['neutron_py'], data['neutron_pz'], data['neutron_e'])

# print the first 10 calculations of the neutron mass
print('The invariant mass of the neutron for the first 10 events in GeV/c^2: ')
print(data['m_neutron'].head(10))

# find the invariant masses of the different combinations

# neutron, the 2 pi plus particles, and pi minus
data['combo1_px'] = data['neutron_px'] + data['pip1_px'] + data['pip2_px'] + data['pim_px']
data['combo1_py'] = data['neutron_py'] + data['pip1_py'] + data['pip2_py'] + data['pim_py']
data['combo1_pz'] = data['neutron_pz'] + data['pip1_pz'] + data['pip2_pz'] + data['pim_pz']
data['combo1_e'] = data['neutron_e'] + data['pip1_e'] + data['pip2_e'] + data['pim_e']

data['m_combo1'] = calc_invariant_mass(data['combo1_px'], data['combo1_py'], data['combo1_pz'], data['combo1_e'])

#  2 pi plus particles and pi minus
data['combo2_px'] = data['pip1_px'] + data['pip2_px'] + data['pim_px']
data['combo2_py'] = data['pip1_py'] + data['pip2_py'] + data['pim_py']
data['combo2_pz'] = data['pip1_pz'] + data['pip2_pz'] + data['pim_pz']
data['combo2_e'] = data['pip1_e'] + data['pip2_e'] + data['pim_e']

data['m_combo2'] = calc_invariant_mass(data['combo2_px'], data['combo2_py'], data['combo2_pz'], data['combo2_e'])

# 1st pi plus and pi minus
data['combo3_px'] = data['pip1_px'] + data['pim_px']
data['combo3_py'] = data['pip1_py'] + data['pim_py']
data['combo3_pz'] = data['pip1_pz'] + data['pim_pz']
data['combo3_e'] = data['pip1_e'] + data['pim_e']

data['m_combo3'] = calc_invariant_mass(data['combo3_px'], data['combo3_py'], data['combo3_pz'], data['combo3_e'])

# 2nd pi plus and pi minus
data['combo4_px'] = data['pip2_px'] + data['pim_px']
data['combo4_py'] = data['pip2_py'] + data['pim_py']
data['combo4_pz'] = data['pip2_pz'] + data['pim_pz']
data['combo4_e'] = data['pip2_e'] + data['pim_e']

data['m_combo4'] = calc_invariant_mass(data['combo4_px'], data['combo4_py'], data['combo4_pz'], data['combo4_e'])

# 2 pi plus particles
data['combo5_px'] = data['pip1_px'] + data['pip2_px']
data['combo5_py'] = data['pip1_py'] + data['pip2_py']
data['combo5_pz'] = data['pip1_pz'] + data['pip2_pz']
data['combo5_e'] = data['pip1_e'] + data['pip2_e']

data['m_combo5'] = calc_invariant_mass(data['combo5_px'], data['combo5_py'], data['combo5_pz'], data['combo5_e'])

# neutron and 1st pi plus
data['combo6_px'] = data['neutron_px'] + data['pip1_px']
data['combo6_py'] = data['neutron_py'] + data['pip1_py']
data['combo6_pz'] = data['neutron_pz'] + data['pip1_pz']
data['combo6_e'] = data['neutron_e'] + data['pip1_e']

data['m_combo6'] = calc_invariant_mass(data['combo6_px'], data['combo6_py'], data['combo6_pz'], data['combo6_e'])

# neutron and 2nd pi plus
data['combo7_px'] = data['neutron_px'] + data['pip2_px']
data['combo7_py'] = data['neutron_py'] + data['pip2_py']
data['combo7_pz'] = data['neutron_pz'] + data['pip2_pz']
data['combo7_e'] = data['neutron_e'] + data['pip2_e']

data['m_combo7'] = calc_invariant_mass(data['combo7_px'], data['combo7_py'], data['combo7_pz'], data['combo7_e'])

# neutron and pi minus
data['combo8_px'] = data['neutron_px'] + data['pim_px']
data['combo8_py'] = data['neutron_py'] + data['pim_py']
data['combo8_pz'] = data['neutron_pz'] + data['pim_pz']
data['combo8_e'] = data['neutron_e'] + data['pim_e']

data['m_combo8'] = calc_invariant_mass(data['combo8_px'], data['combo8_py'], data['combo8_pz'], data['combo8_e'])

ax = data["m_combo1"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of Neutron, $\pi^+_1$, $\pi^+_2$, and $\pi^-$ Combination')
plt.savefig('hist_combo1.png')

plt.clf()
ax = data["m_combo2"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of $\pi^+_1$, $\pi^+_2$, and $\pi^-$ Combination')
plt.savefig('hist_combo2.png')

plt.clf()
ax = data["m_combo3"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of $\pi^+_1$ and $\pi^-$ Combination')
plt.savefig('hist_combo3.png')

plt.clf()
ax = data["m_combo4"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of $\pi^+_2$ and $\pi^-$ Combination')
plt.savefig('hist_combo4.png')

plt.clf()
ax = data["m_combo5"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of $\pi^+_1$ and $\pi^+_2$ Combination')
plt.savefig('hist_combo5.png')

plt.clf()
ax = data["m_combo6"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of Neutron and $\pi^+_1$ Combination')
plt.savefig('hist_combo6.png')

plt.clf()
ax = data["m_combo7"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of Neutron and $\pi^+_2$ Combination')
plt.savefig('hist_combo7.png')

plt.clf()
ax = data["m_combo8"].hist(bins=100)
ax.set_xlim(0., 2.)
ax.set_xlabel("Mass (GeV)")
ax.set_ylabel("Counts / 20 MeV")
plt.title(r'Invariant 4-Momenta Mass of Neutron and $\pi^-$ Combination')
plt.savefig('hist_combo8.png')
