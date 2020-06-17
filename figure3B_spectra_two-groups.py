"""
Create a figure showing the MRS spectra for a set of participants.

Participant IDs and group category should be in a TSV file entitled participants.tsv located in the
project directory.

This example uses MEGA-PRESS difference spectra created with Gannet v3.

Created by NWD, 2020-01-31
Modified by VHT, 2020-02-07

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Project directory
data_dir = '/home/MRS_project/'

# Directory to create figures in
fig_dir = os.path.join(data_dir,'figures')

# Create figure directory if missing
if not os.path.isdir(fig_dir):
  os.mkdir(fig_dir)

# Column names in the participants.tsv file for participant IDs and group membership
ID_header = 'participant_id'
group_header = 'group'

# Naming of the group categories:
group_name_1 = 'Group1'
group_name_2 = 'Group2'

# Load in the participant IDs and group information
subjects = pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]
groups =  pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[group_header]
n_subs_1 = sum(isinstance(name, str) for name in groups if name==group_name_1)
n_subs_2 = sum(isinstance(name, str) for name in groups if name==group_name_2)

# Spectra filename
spec_file = 'spectrum.txt'

# Spectra frequency filename
freq_file = 'spectrum_frequencies.txt'

# Display range - indices to show only the desired region of the spectra
# This will vary between data types and analysis software
disp_range = [17500,23000]

# Colour to make the individual spectra - should be in a format compatible with matplotlib
spec_colour_1 = 'red'
spec_colour_2 = 'blue'

# Load in the spectum frequencies
freq = np.loadtxt(os.path.join(data_dir,subjects[0],'mrs',freq_file))
freq_len = freq.shape[-1]

# Load in spectra
spec_1 = np.zeros((n_subs_1,freq_len))
spec_2 = np.zeros((n_subs_2,freq_len))

idx1 = 0
idx2 = 0
for i,sub in enumerate(subjects):
  if groups[i]==group_name_1:
    spec_1[idx1,:] = np.loadtxt(os.path.join(data_dir,subjects[i],'mrs',spec_file))
    idx1 = idx1+1
  if groups[i]==group_name_2:
    spec_2[idx2,:] = np.loadtxt(os.path.join(data_dir,subjects[i],'mrs',spec_file))
    idx2 = idx2+1

# Calculate group mean
mean_spec_1 = np.mean(spec_1, axis=0)
mean_spec_2 = np.mean(spec_2, axis=0)

# Plot the figure
fig = plt.figure()
fig.set_size_inches(3,2)
ax1 = plt.subplot(111)
ax1.spines['top'].set_visible(False) # Some cosmetic commands
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.get_xaxis().tick_bottom()
ax1.get_yaxis().tick_left()
ax1.tick_params(axis='x', direction='out')
ax1.tick_params(axis='y', length=0)
ax1.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax1.set_axisbelow(True)
for i in range(n_subs_1): # Plot individual spectra
    ax1.plot(freq[disp_range[0]:disp_range[1]], spec_1[i,disp_range[0]:disp_range[1]],
      linewidth=0.4, alpha=0.3, color=spec_colour_1)
for i in range(n_subs_2): # Plot individual spectra
    ax1.plot(freq[disp_range[0]:disp_range[1]], spec_2[i,disp_range[0]:disp_range[1]],
      linewidth=0.4, alpha=0.3, color=spec_colour_2)
ax1.plot(freq[disp_range[0]:disp_range[1]], mean_spec_1[disp_range[0]:disp_range[1]],
  linewidth=1, alpha=0.9, color=spec_colour_1)
ax1.plot(freq[disp_range[0]:disp_range[1]], mean_spec_2[disp_range[0]:disp_range[1]],
  linewidth=1, alpha=0.9, color=spec_colour_2)
ax1.set_xlabel('ppm',fontsize=8) # Label for x-axix - assumed to be in ppm here
ax1.tick_params(axis='x',labelsize=8)
ax1.set_yticklabels(('')) # Remove the tick labels from the y-axis

plt.gca().invert_xaxis() # Invert the ppm axis (for convention)

# Save the figure
fig.savefig(fig_dir+'mrs_spectra_two-groups.png',bbox_inches='tight',dpi=300)
