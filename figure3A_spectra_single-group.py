"""
Create a figure showing the MRS spectra for a set of participants.

Participant IDs should be in a TSV file entitled participants.tsv located in the
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

# Name of the participant ID column in the participants.tsv file
ID_header='participant_id'

# Load in the participant IDs
subjects = pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]

n_subs = len(subjects)

# Spectra filename
spec_file = 'spectrum.txt'

# Spectra frequency filename
freq_file = 'spectrum_frequencies.txt'

# Display range - indices to show only the desired region of the spectra
# This will vary between data types and analysis software
def find_nearest(x,value):
    idx = (abs(x-value)).argmin()
    return idx

disp_range = [find_nearest(freq,4.2),find_nearest(freq,1.5)]

# Colour to make the individual spectra - should be in a format compatible with matplotlib
spec_colour = 'black'
spec_color_mean = 'red'

# Load in the spectum frequencies
freq = np.loadtxt(os.path.join(data_dir,subjects[0],'mrs',freq_file))
freq_len = freq.shape[-1]

# Load in spectra
all_spec = np.zeros((n_subs,freq_len))
for i,sub in enumerate(subjects):
    all_spec[i,:] = np.loadtxt(os.path.join(data_dir,subjects[i],'mrs',spec_file))

# Calculate group mean
mean_spec = np.mean(all_spec, axis=0)

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
for i in range(n_subs): # Plot individual spectra
    ax1.plot(freq[disp_range[0]:disp_range[1]], all_spec[i,disp_range[0]:disp_range[1]],
      linewidth=0.3, alpha=0.3, color=spec_colour)
ax1.plot(freq[disp_range[0]:disp_range[1]], mean_spec[disp_range[0]:disp_range[1]],
  linewidth=0.8, alpha=0.9, color=spec_color_mean)
ax1.set_xlabel('ppm',fontsize=8) # Label for x-axix - assumed to be in ppm here
ax1.tick_params(axis='x',labelsize=8)
ax1.set_yticklabels(('')) # Remove the tick labels from the y-axis

plt.gca().invert_xaxis() # Invert the ppm axis (for convention)

# Save the figure
fig.savefig(fig_dir+'mrs_spectra_single-group.png',bbox_inches='tight',dpi=300)
