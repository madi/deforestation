
'''
conda activate /eos/jeodpp/home/users/leomarg/miniconda/envs/my-demo
export PYTHONPATH=/eos/jeodpp/home/users/leomarg/miniconda/envs/my-demo/lib/python3.6/site-packages:$PYTHONPATH
python3
'''


import gdal
import numpy as np
import pandas as pd
import time, os, glob
import matplotlib.pylab as plt
import matplotlib.animation
from sar_conversions import *

pol="vh"

datadirectory="/media/madi/TOSHIBA EXT/S1/S1_cropped"


if pol=="vv":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_vv.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_cropped/s1_stack_vv.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/bands_plots_like"
elif pol=="vh":
    datefile="/media/madi/TOSHIBA EXT/S1/S1_files/S1_vh.dates"
    imagefile="/media/madi/TOSHIBA EXT/S1/S1_cropped/s1_stack_vh.vrt"
    dest_folder="/media/madi/TOSHIBA EXT/S1/bands_plots_cross"
else:
    print("Data for selected polarization are not available.")


#-----------------------------------------------------------------------

def plotAmpwHist(bandn, pol):
    '''
    Plot amplitude (Uncalibrated DN values) with histogram
    '''
    fig=plt.figure(figsize=(16,8))
    ax1=fig.add_subplot(121)
    ax2=fig.add_subplot(122)
    # First plot: image
    raster=img.GetRasterBand(bandn).ReadAsArray()
    ax1.imshow(raster,cmap='gray',
               vmin=np.nanpercentile(raster,10),
               vmax=np.nanpercentile(raster,90))
    ax1.set_title('Image band %s %s' %(bandn, tindex[bandn-1].date()))
    # Second plot: histogram
    h=ax2.hist(raster.flatten(),bins=100,
               range=(np.nanpercentile(raster,10),np.nanpercentile(raster,90)))
    ax2.xaxis.set_label_text('Amplitude (Uncalibrated DN values)')
    ax2.set_title("Histogram band %s %s pol %s" %(bandn, 
                   tindex[bandn-1].date(), pol))
    plt.show()
    #plt.savefig(dest_folder+os.sep+"Histogram_band_%s_%s_%s.png" %(bandn, tindex[bandn-1].date(), pol))
    plt.close()
    # Flush cache
    raster=None
    return 0

#-----------------------------------------------------------------------

def CalcDataVolume(img):
    '''
    Calculate data volume. You can compare with avail RAM
    '''
    Nbands = img.RasterCount    # Number of bands
    Npixels = img.RasterXSize   # Number of pixels
    Nlines = img.RasterYSize    # Number of lines
    bxp = 4 # bites per pixel for Float32
    return (Nbands * Npixels * Nlines * bxp)/(1024^3)

#-----------------------------------------------------------------------

def CalcAvailRAM():
    '''
    Returns available RAM
    '''
    import psutil
    mem=dict(psutil.virtual_memory()._asdict())
    return mem['total']/(1e+9) # GB
 
#-----------------------------------------------------------------------

def PrintLookUpBandDate(imagefile):
    '''
    Create lookup table band <-> date
    '''
    j=1
    print('Bands and dates for ',imagefile)
    for i in tindex:
        print("{:4d} {}".format(j, i.date()),end=' ')
        j+=1
        if j%5==1: print()
    return 0

#-----------------------------------------------------------------------

def plotComparisonRepr(bandn, pol):
    '''
    Create a four-part figure comparing the effect of the representation
    of the backscatter values in the DN, amplitude,power and dB scale
    '''
    fig=plt.figure(figsize=(16,16))
    fig.suptitle("Band %s %s pol %s" %(bandn, tindex[bandn-1].date(), \
                  pol), fontsize=14)
    ax1=fig.add_subplot(221)
    ax2=fig.add_subplot(222)
    ax3=fig.add_subplot(223)
    ax4=fig.add_subplot(224)
    # DN
    rasterDN=img.GetRasterBand(bandn).ReadAsArray()
    rasterDN[rasterDN<=0]=0.0001
    # deciBel
    rasterdB=amp2dB(rasterDN)
    # power
    rasterPwr=dB2pwr(rasterdB)
    # amplitude
    rasterAmp=pwr2amp(rasterPwr)
    # DN
    ax1.imshow(rasterDN,cmap='gray',
               vmin=np.percentile(rasterDN,10),
               vmax=np.percentile(rasterDN,90))
    # amplitude
    ax2.imshow(rasterAmp,cmap='gray',
               vmin=np.percentile(rasterAmp,10),
               vmax=np.percentile(rasterAmp,90))
    # power
    ax3.imshow(rasterPwr,cmap='gray',
               vmin=np.percentile(rasterPwr,10),
               vmax=np.percentile(rasterPwr,90))
    # deciBel
    ax4.imshow(rasterdB,cmap='gray',
               vmin=np.percentile(rasterdB,10),
               vmax=np.percentile(rasterdB,90))
    ax1.set_title('DN')
    ax2.set_title('Amplitude Scaled')
    ax3.set_title('Power Scaled')
    ax4.set_title('dB Scaled')
    #plt.savefig(dest_folder+os.sep+"band_%s_%s_%s.png" %(bandn, tindex[bandn-1].date(), pol))
    plt.show()
    plt.close()
    return 0

#-----------------------------------------------------------------------

def compareHist(bandn, pol):
    '''
    Compare histograms of the amplitude, power and dB scaled data
    '''
    fig=plt.figure(figsize=(16,4))
    fig.suptitle('Comparison of Histograms of SAR Backscatter in different scales \
    Band %s %s pol %s' %(bandn, tindex[bandn-1].date(), pol), \
                  fontsize=14)
    ax1=fig.add_subplot(131)
    ax2=fig.add_subplot(132)
    ax3=fig.add_subplot(133)
    # DN
    rasterDN=img.GetRasterBand(bandn).ReadAsArray()
    rasterDN[rasterDN<=0]=0.0001
    # deciBel
    rasterdB=amp2dB(rasterDN)
    # power
    rasterPwr=dB2pwr(rasterdB)
    # amplitude
    rasterAmp=pwr2amp(rasterPwr)
    ax1.hist(rasterAmp.flatten(),
             bins=100,range=(np.percentile(rasterAmp,5),
             np.percentile(rasterAmp,95)))
    ax2.hist(rasterPwr.flatten(),
             bins=100,range=(np.percentile(rasterPwr,5),
             np.percentile(rasterPwr,95)))
    ax3.hist(rasterdB.flatten(),
             bins=100,range=(np.percentile(rasterdB,5),
             np.percentile(rasterdB,95)))
    # Mean, median and stdev
    amp_mean=rasterAmp.mean()
    amp_std=rasterAmp.std()
    pwr_mean=rasterPwr.mean()
    pwr_std=rasterPwr.std()
    dB_mean=rasterdB.mean()
    dB_std=rasterdB.std()
    # add lines for mean and median
    ax1.axvline(amp_mean, color='red', label='Mean')
    ax1.axvline(np.median(rasterAmp), color='blue', label='Median')
    ax2.axvline(pwr_mean, color='red')
    ax2.axvline(np.median(rasterPwr), color='blue')
    ax3.axvline(dB_mean, color='red')
    ax3.axvline(np.median(rasterdB), color='blue')
    # add lines for 1 stddev
    ax1.axvline(amp_mean-amp_std, color='gray', label='1 $\sigma$')
    ax1.axvline(amp_mean+amp_std, color='gray')
    #ax2.axvline(pwr_mean-pwr_std, color='gray')
    #ax2.axvline(pwr_mean+pwr_std, color='gray')
    ax3.axvline(dB_mean-dB_std, color='gray')
    ax3.axvline(dB_mean+dB_std, color='gray')
    # set titles
    ax1.set_title('Amplitude Scaled')
    ax2.set_title('Power Scaled')
    ax3.set_title('dB Scaled')
    ax1.legend()
    for ax in fig.axes:
        plt.sca(ax)
        plt.xticks(rotation=45)
    plt.show()
    #plt.savefig(dest_folder+os.sep+"Hist_comparison_band_%s_%s_%s.png" %(bandn, tindex[bandn-1].date(), pol))
    plt.close()
    return 0
    
#-----------------------------------------------------------------------

def createAnim(imagefile):
    '''
    Create png files for animation animation
    '''
    for bandn in range(1, img.RasterCount):
        raster=img.GetRasterBand(bandn).ReadAsArray()
        vmin=np.percentile(raster.flatten(),5)
        vmax=np.percentile(raster.flatten(),95)
        fig=plt.figure(figsize=(10,10))
        ax=fig.add_subplot(111)
        ax.axis('off')
        im=ax.imshow(raster, cmap='gray', vmin=vmin, vmax=vmax)
        ax.set_title('%s' %(tindex[bandn-1].date()))
        plt.show()
        #plt.savefig(dest_folder+os.sep+"anim_%s.png" %(tindex[bandn-1].date()))
        plt.close()
    return 0
    
#-----------------------------------------------------------------------

os.chdir(datadirectory)
os.getcwd()
glob.glob("*.vrt")

# Read from the dates file the dates in the time series and make a pandas date index

dates=open(datefile).readlines()
tindex=pd.DatetimeIndex(dates)

# Image data

img=gdal.Open(imagefile)

#-----------------------------------------------------------------------

# Print look-up table date <-> band

# j=1
# print('Bands and dates for ', imagefile)
# for i in tindex:
    # print("{:4d} {}".format(j, i.date()), end=' ')
    # j+=1
    # if j%5==1:print()

#-----------------------------------------------------------------------

# Set band number

bandn=499

#-----------------------------------------------------------------------

# Reading data from an image band

# raster=img.GetRasterBand(bandn).ReadAsArray()

#-----------------------------------------------------------------------

# Plot amplitude (Uncalibrated DN values) with histogram

plotAmpwHist(bandn,pol) 

#-----------------------------------------------------------------------

# Plot amplitude (Uncalibrated DN values) with histogram
# Iterating over all bands

# for bandn in range(1, img.RasterCount):
    # plotAmpwHist(bandn)

#-----------------------------------------------------------------------

# Calculate data volume and compare with avail RAM

# datavol=CalcDataVolume(img)
# print ("Data volume [GB] %s" %(datavol))
# ram=CalcAvailRAM()
# print ("Available RAM [GB] %s" %(ram))

#-----------------------------------------------------------------------

# Create a four-part figure comparing the effect of the representation
# of the backscatter values in the DN, amplitude,power and dB scale

# plotComparisonRepr(bandn,pol)

#-----------------------------------------------------------------------

# Create a 3-part plot to compare histograms of the amplitude, power and 
# dB scaled data

# compareHist(bandn,pol)

#-----------------------------------------------------------------------

# Create png files for animation animation

# createAnim(imagefile)

#-----------------------------------------------------------------------

# Generate an 8-bit scaled dB image

# rasterDN=img.GetRasterBand(bandn).ReadAsArray()
# rasterDB = rescale2(rasterDN)
# fig=plt.figure()
# ax=fig.add_subplot(111)
# # First plot: image
# raster = rasterDB
# ax.imshow(raster, cmap='gray', 
          # vmin=np.percentile(raster,10),
          # vmax=np.percentile(raster,90))
# plt.show()
# plt.close()
# raster=None

#-----------------------------------------------------------------------

# Create multi-temporal color composite
# Bands chosen for cross-pol stack: 
# 7 (2014-12-01), 151 (2016-12-04), 464 (2018-12-03)
# 59 (2015-08-12), 129 (2016-08-16), 252 (2018-08-11)

# import skimage
# from skimage import data, exposure, img_as_float

# rgb_bands=(59,129,252)
# arrays=[]
# for bandn in rgb_bands:
    # rasterDN=img.GetRasterBand(bandn).ReadAsArray() 
    # arrays.append(rasterDN)
    
# rgb=np.stack(arrays, axis=2)
# rgb_dates=(tindex[rgb_bands[0]-1],tindex[rgb_bands[1]-1],tindex[rgb_bands[2]-1])

# # Image equalization
# rgb_equalized = rgb.copy()
# for i in range(rgb.shape[2]):
    # image=rgb[:,:,i]
    # img_eq = exposure.equalize_hist(image)
    # rgb_equalized[:,:,i] = img_eq

# # Image stretching
# rgb_stretch = rgb.copy()
# for i in range(rgb.shape[2]):
    # image=rgb[:,:,i]
    # p2, p98 = np.percentile(image, (2, 98))
    # img_st = exposure.rescale_intensity(image, in_range=(p2, p98))
    # rgb_stretch[:,:,i] = img_st


# fig=plt.figure()
# fig.suptitle('Multi-temporal Sentinel-1 backscatter image R:{} G:{} B:{}'
            # .format(rgb_dates[0].strftime('%Y-%m-%d'),
            # rgb_dates[1].strftime('%Y-%m-%d'),
            # rgb_dates[2].strftime('%Y-%m-%d')), fontsize=14)
# ax1=fig.add_subplot(121)
# ax2=fig.add_subplot(122)
# ax1.imshow(rgb_stretch)
# ax1.set_title('Contrast stretching')
# ax2.imshow(rgb_equalized)
# ax2.set_title('Histogram equalization')
# plt.show()
# plt.close()





