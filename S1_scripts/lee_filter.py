
"""
https://stackoverflow.com/questions/39785970/speckle-lee-filter-in-python

python3 main.py

"""

import matplotlib.pyplot as plt
import numpy as np

from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance

def lee_filter(img, size=20):
    img_mean = uniform_filter(img, (size, size))
    img_sqr_mean = uniform_filter(img**2, (size, size))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + overall_variance)
    print(overall_variance)
    img_output = img_mean + img_weights * (img - img_mean)
    return img_output

def plotLee(img, size=20, vmin=None, vmax=None):
    fig = plt.figure(figsize=(16,8)) 
    ax1 = fig.add_subplot(121)  
    ax2 = fig.add_subplot(122) 
    vmin=np.nanpercentile(img,10) if vmin==None else vmin
    vmax=np.nanpercentile(img,90) if vmax==None else vmax
    ax1.imshow(img, vmin=vmin, vmax=vmax, cmap='gray')
    ax2.imshow(lee_filter(img, size), vmin=vmin, vmax=vmax, cmap='gray')
    plt.show()




