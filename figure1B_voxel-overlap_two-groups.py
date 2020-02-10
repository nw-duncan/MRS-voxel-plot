"""
Create a figure showing the overlap between the MRS voxels of a set of participants. 

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
from matplotlib import ticker
import matplotlib.gridspec as gridspec

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
group_header='Group'

# Naming of the group categories:
group_name_1='Group1'
group_name_2='Group2'

# Load in the participant IDs and group information
subjects =  pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[ID_header]
groups =  pd.read_csv(data_dir+'participants.tsv', delimiter='\t')[group_header]
n_subs_1 = sum(isinstance(name, str) for name in groups if name==group_name_1)
n_subs_2 = sum(isinstance(name, str) for name in groups if name==group_name_2)



# Load the MRS mask affine matrix and dimensions
def get_mask_info(fpath):
  tmp = ni.load(fpath)
  aff = tmp.affine
  dims = tmp.shape
  return(aff,dims)

mask_aff, mask_dims = get_mask_info(os.path.join(data_dir,subjects[0],'mrs',mask_file))

# Load mask data for participants in each group
mask_data_group_1 = np.zeros(np.hstack((n_subs_1,mask_dims)))
mask_data_group_2 = np.zeros(np.hstack((n_subs_2,mask_dims)))

idx1=0
idx2=0
for i in range(len(subjects)):
    if groups[i]==group_name_1:
        mask_data_group_1[idx1,:,:,:] = ni.load(os.path.join(data_dir,subjects[i],'mrs',mask_file)).get_data()
        idx1=idx1+1
    if groups[i]==group_name_2:
        mask_data_group_2[idx2,:,:,:] = ni.load(os.path.join(data_dir,subjects[i],'mrs',mask_file)).get_data()
        idx2=idx2+1

# Calculate the voxel density map
density_1 = np.sum(mask_data_group_1, axis = 0)
density_1 = (density_1/n_subs_1)*100
density_2 = np.sum(mask_data_group_2, axis = 0)
density_2 = (density_2/n_subs_2)*100

# Create NIFTI image for density map
density_map_1 = ni.Nifti1Image(density_1,mask_aff)
density_map_2 = ni.Nifti1Image(density_2,mask_aff)

# Plot the figure
fig = plt.figure()
fig.set_size_inches(6,3)

gs = gridspec.GridSpec(1, 3,width_ratios=[9,1,1])
ax1 = plt.subplot(gs[0])

display=plotting.plot_glass_brain(None, threshold=0, colorbar=False, axes=ax1, display_mode='xz',alpha=0.5)
display.add_contours(density_map_1, cmap='Reds',alpha=0.7)
display.add_contours(density_map_2, cmap='Blues',alpha=0.7)

ax2 = plt.subplot(gs[1])
a = np.array([[0,1]])
img = plt.imshow(a, cmap="Reds",axes=ax2)
ax2.set_visible(False)
plt.colorbar(ax=ax2)

ax3 = plt.subplot(gs[2])
a = np.array([[0,1]])
img = plt.imshow(a, cmap="Blues",axes=ax3)
ax3.set_visible(False)
plt.colorbar(ax=ax3)

# Adjust the scientific notation in the colorbars
for ax in plt.gcf().axes:
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))

# Save the figure
fig.savefig(fig_dir+'figure_voxel_density_map_two-groups.png',bbox_inches='tight',dpi=300)

# Save density map NIFTI files
density_map_1.to_filename(fig_dir+'voxel_density_map_group_1.nii.gz')
density_map_2.to_filename(fig_dir+'voxel_density_map_group_2.nii.gz')