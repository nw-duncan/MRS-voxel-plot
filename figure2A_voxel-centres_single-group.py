"""
Create a figure showing the voxel centroids for a set of participants.

Each participant requires a mask image in standard space.

Participant IDs should be in a TSV file entitled participants.tsv located in the
project directory.

Created by NWD, 2020-01-31

"""


import os
import numpy as np
import pandas as pd
import nibabel as ni
import matplotlib.pyplot as plt
from nilearn import plotting

# Project directory
data_dir = '/home/MRS_project/'

# Directory to create figures in
fig_dir = os.path.join(data_dir,'figures')

# Create figure directory if missing
if not os.path.isdir(fig_dir):
  os.mkdir(fig_dir)

# Mask filename
mask_file = 'mask_mni.nii.gz'

# Naming of the headers of the participants.tsv file
ID_header='Participant_ID'

# Colour to make the centroid markers - should be in a format compatible with matplotlib
node_colour = 'red'

# Load in the participant IDs
subjects = pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]
n_subs = len(subjects)

# Load all masks into a list
all_masks = []
for i, sub in enumerate(subjects):
    all_masks.append(ni.load(os.path.join(data_dir,sub,'mrs',mask_file)))

# Calculate the coordinates of the centroids
all_centres = np.zeros((n_subs,3))
for i in range(n_subs):
    all_centres[i,:] = plotting.find_xyz_cut_coords(all_masks[i])

# Create a dummy adjacency matrix
adjacency_matrix = np.zeros((n_subs,n_subs))

# Plot the figure
fig = plt.figure()
fig.set_size_inches(5,3)
axes1 = plt.subplot(111)
plotting.plot_connectome(adjacency_matrix=adjacency_matrix, node_coords=all_centres,
  node_size=50, node_color=node_colour, display_mode='xz', node_kwargs={'alpha':0.3},
  axes=axes1)

# Save the figure
fig.savefig(fig_dir+'mask_centroids_single-group.png',bbox_inches='tight',dpi=300)