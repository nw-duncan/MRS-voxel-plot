"""
Create a figure showing the overlap between the MRS voxels of a set of participants.

Each participant requires a mask image in standard space.

Participant IDs should be in a TSV file entitled participants.tsv located in the
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
from matplotlib import ticker

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

# Load in the participant IDs
subjects = pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]

n_subs = len(subjects)

# Load the MRS mask affine matrix and dimensions
def get_mask_info(fpath):
  tmp = ni.load(fpath)
  aff = tmp.affine
  dims = tmp.shape
  return(aff,dims)

mask_aff, mask_dims = get_mask_info(os.path.join(data_dir,subjects[0],'mrs',mask_file))

# Load mask data for all participants
all_mask_data = np.zeros(np.hstack((n_subs,mask_dims)))
for i,sub in enumerate(subjects):
  all_mask_data[i,:,:,:] = ni.load(os.path.join(data_dir,sub,'mrs',mask_file)).get_data()

# Calculate the voxel density map
density = np.sum(all_mask_data, axis = 0)
density = (density/n_subs)*100

# Create NIFTI image for density map
density_map = ni.Nifti1Image(density,mask_aff)

# Plot the figure
fig = plt.figure()
fig.set_size_inches(6,3)
ax1 = plt.subplot(111)
plotting.plot_glass_brain(density_map, threshold=0, colorbar=True, axes=ax1, cmap='autumn', display_mode='xz')

# Adjust the scientific notion in the colorbar
for ax in plt.gcf().axes:
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))

# Save the figure
fig.savefig(fig_dir+'figure_voxel_density_map_single-group.png',bbox_inches='tight',dpi=300)

# Save density map NIFTI file
density_map.to_filename(fig_dir+'voxel_density_map_single-group.nii.gz')