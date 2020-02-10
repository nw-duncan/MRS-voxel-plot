# MRS-voxel-plot
Example code to create informative MRS voxel and spectra figures for publication.  
#### Figure type 1 - MRS voxel overlaps 
![MRS voxel overlap](example-figures/voxel-density-map_single-group.png)  
Present the overlap in MRS voxels for all participants in a single or multiple groups.  
#### Figure type 2 - MRS voxel centroids
![MRS voxel centroids](example-figures/mask-centroids_two-groups.png)  
Calculate and show MRS voxel centroids for all participants in single or multiple groups.  
#### Figure type 3 - MRS spectra  
![MRS spectra](example-figures/mrs-spectra_single-group.png)  
Present individual and group average MRS spectra. 


# Dependencies
- Numpy (https://numpy.org)
- Matplotlib (https://matplotlib.org)
- Nilearn (https://nilearn.github.io)
- Pandas (https://pandas.pydata.org)

# Data organisation
The scripts assume that your data are in folders organised in a manner similar to the BIDS standard (https://bids.neuroimaging.io/).  

Participant IDs and group labels (where relevant) should be in a TSV file that conforms to this standard.

# Acknowledgement

Please also cite https://www.frontiersin.org/articles/10.3389/fninf.2014.00014/full when using nilearn. 
