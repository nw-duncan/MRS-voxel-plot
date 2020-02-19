"""
Create a figure showing the voxel centroids for a set of participants 

Each participant requires a mask image in standard space.

Participant IDs and group category should be in a TSV file entitled participants.tsv located in the
project directory.

Created by NWD, 2020-01-31
Modified by VHT, 2020-02-07

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

# Name of the participant ID and group membership columns in the participants.tsv file
ID_header = 'participant_id'
group_header = 'group'

# Naming of the group categories:
group_name_1 = 'Group1'
group_name_2 = 'Group2'

# Colour to make the centroid markers - should be in a format compatible with matplotlib
node_colour_1 = 'red'
node_colour_2 = 'blue'

# Load in the participant IDs and group information
subjects = pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]
groups =  pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[group_header]
n_subs_1 = sum(isinstance(name, str) for name in groups if name==group_name_1)
n_subs_2 = sum(isinstance(name, str) for name in groups if name==group_name_2)

# Load all masks into a list
masks_1 = []
masks_2 = []
for i, sub in enumerate(subjects):
  if groups[i]==group_name_1:
    masks_1.append(ni.load(os.path.join(data_dir,sub,'mrs',mask_file)))
  if groups[i]==group_name_2:
    masks_2.append(ni.load(os.path.join(data_dir,sub,'mrs',mask_file)))

# Calculate the coordinates of the centroids
centres_1 = np.zeros((n_subs_1,3))
centres_2 = np.zeros((n_subs_2,3))
for i in range(n_subs_1):
    centres_1[i,:] = plotting.find_xyz_cut_coords(masks_1[i])
for i in range(n_subs_2):
    centres_2[i,:] = plotting.find_xyz_cut_coords(masks_2[i]) 

# Create a dummy adjacency matrix
adjacency_matrix_1 = np.zeros((n_subs_1,n_subs_1))
adjacency_matrix_2 = np.zeros((n_subs_2,n_subs_2))
# Plot the figure
fig = plt.figure()
fig.set_size_inches(5,3)
axes1 = plt.subplot(111)
plotting.plot_connectome(adjacency_matrix=adjacency_matrix_1, node_coords=centres_1,
  node_size=50, node_color=node_colour_1, display_mode='xz', node_kwargs={'alpha':0.3},
  axes=axes1)
plotting.plot_connectome(adjacency_matrix=adjacency_matrix_2, node_coords=centres_2,
  node_size=50, node_color=node_colour_2, display_mode='xz', node_kwargs={'alpha':0.3},
  axes=axes1)

# Save the figure
fig.savefig(fig_dir+'mask_centroids_two-groups.png',bbox_inches='tight',dpi=300)
