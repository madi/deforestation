import gdal
import numpy as np
import pandas as pd
import time, os, glob
import matplotlib.pylab as plt
from astropy.visualization import (MinMaxInterval, SqrtStretch,
                                   ImageNormalize, LogStretch,
                                   simple_norm)

def showImage(raster,tindex,bandnbr,vmin=None,vmax=None):
    fig = plt.figure(figsize=(16,8))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    vmin=np.nanpercentile(raster,10) if vmin==None else vmin
    vmax=np.nanpercentile(raster,90) if vmax==None else vmax
    ax1.imshow(raster,cmap='gray',
               vmin=vmin,
               vmax=vmax)
    ax1.set_title('Image Band {} {}'.format(bandnbr,
                  tindex[bandnbr-1].date()))
    ax1.xaxis.set_label_text(
             'Linear stretch Min={} Max={}'.format(vmin,vmax))
    
    # if np.isnan(np.sum(raster)):
        # raster = raster[~np.isnan(raster)] 
    
    h = ax2.hist(raster.flatten(),bins=100,range=(vmin,vmax))
    ax2.xaxis.set_label_text('Amplitude')
    ax2.set_title('Histogram Band {} {}'.format(bandnbr,
                  tindex[bandnbr-1].date()))
    plt.show()
    plt.close()


def showNormImg(raster,tindex=None,bandnbr=None,vmin=None,vmax=None):
    '''
    Plot normalized image
    '''
    image=np.nan_to_num(raster)
    vmin=np.nanpercentile(raster,10) if vmin==None else vmin
    vmax=np.nanpercentile(raster,90) if vmax==None else vmax
    # norm = ImageNormalize(image, interval=MinMaxInterval(),
                      # stretch=SqrtStretch())
    norm = ImageNormalize(image, interval=MinMaxInterval(),
                      stretch=LogStretch())
    # norm = simple_norm(image, 'sqrt')
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # im = ax.imshow(image, origin='lower', norm=norm)
    im = ax.imshow(image, cmap='PiYG', origin='lower', norm=norm, 
               vmin=vmin,
               vmax=vmax)
    ax.set_title('Image Band {} {} , normalized representation'.format(bandnbr,
                  tindex[bandnbr-1].date()))
    fig.colorbar(im)
    plt.show()
    plt.close()
    
def showLogRatioChange(raster,tindex,bandnbr_r,bandnbr_i,vmin=None,vmax=None):
    fig = plt.figure(figsize=(16,8))
    fig.suptitle('Log-ratio change between {} ({}) and {} ({})'.format(
                  bandnbr_r, tindex[bandnbr_r-1].date(),
                  bandnbr_i, tindex[bandnbr_i-1].date()))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    #Fig 1
    #vmin=np.nanpercentile(raster,5) if vmin==None else vmin
    #vmax=np.nanpercentile(raster,95) if vmax==None else vmax
    ax1.imshow(raster,cmap='gray',
               vmin=vmin,
               vmax=vmax)
    ax1.set_title('Log-ratio change')
    ax1.xaxis.set_label_text(
             'Linear stretch Min={} Max={}'.format(vmin,vmax))
    # Fig 2
    image=np.nan_to_num(raster)
    vmin=np.nanpercentile(raster,10) if vmin==None else vmin
    vmax=np.nanpercentile(raster,90) if vmax==None else vmax
    # norm = ImageNormalize(image, interval=MinMaxInterval(),
                      # stretch=SqrtStretch())
    norm = ImageNormalize(image, interval=MinMaxInterval(),
                      stretch=LogStretch())
    # norm = simple_norm(image, 'sqrt')
    # im = ax2.imshow(image, origin='lower', norm=norm)
    im = ax2.imshow(image, cmap='PiYG', norm=norm, 
               vmin=vmin,
               vmax=vmax)
    ax2.set_title('Normalized representation')
    ax2.xaxis.set_label_text(
             'Linear stretch Min={} Max={}'.format(vmin,vmax))
    fig.colorbar(im)
    
    plt.show()
    plt.close()
