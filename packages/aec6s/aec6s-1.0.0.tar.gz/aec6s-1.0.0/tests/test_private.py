

# %matplotlib qt


# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import aec6s




# S2
file = '/Users/yw/Local_storage/GLORIA/240420 Vermote approach/S2A_MSI_2015_09_12_10_17_24_T32TPR_L2R_copy.nc'

# test no data 

# file = '/Users/yw/Local_storage/temp_OSD_test/ACed/20230928/S2B_MSI_2023_09_28_15_44_58_T17MNP_L2R.nc'


# L8
file = '/Users/yw/Local_storage/GLORIA/240420 Vermote approach/L8_OLI_2018_07_03_15_25_47_012030_L2R_copy.nc'




anci_folder = '/Users/yw/Local_storage/GLORIA/240420 Vermote approach/anci' 

username = 'Isa1990'
password = 'Aii_123_!!@@'


aec6s.run(file, anci_folder, username, password, overwrite=False)




'''

import matplotlib.pyplot as plt

# Create a heatmap to visualize the matrix to understand the values
plt.imshow(PSF, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.title("Point-Spread Function (101x101)")
plt.show() 



plt.imshow(image, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show() 

plt.imshow(image_conv, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show() 


plt.imshow(output, cmap='viridis', interpolation='nearest')
plt.colorbar()
plt.show() 



'''




