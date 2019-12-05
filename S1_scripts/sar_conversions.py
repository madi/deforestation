
import numpy as np

def DN2dB_convFactor(rasterDN):
    '''
    Convert amplitude to dB (logarithmic decibel) 
    TODO: find source of this formula
    As per widely used convention SAR backscatter data are often stored 
    in 16bit unsigned integer values as linearly scaled amplitude data 
    (referred to below as digital numbers DN), conversion to dB scale 
    from the linear scaled amplitues is performed with a standard calibration 
    factor of -83 dB. This is how ALOS SAR data are distributed by JAXA, 
    how Earth Big Data LLC produces all SAR data including Sentinel-1 data
    '''
    rasterdB = 20 * np.log10(rasterAmp) - 83
    return rasterdB
    
#-----------------------------------------------------------------------

def DN2dB(rasterDN):
    '''
    Convert Digital Number to dB (logarithmic decibel) 
    '''
    rasterdB = 10. * np.log10(rasterDN)
    return rasterdB
    
#-----------------------------------------------------------------------

def Amp2I(rasterdB):
    '''
    Convert from Amplitude to Intensity
    '''
    rasterI = rasterAmp * rasterAmp
    return rasterI
    
#-----------------------------------------------------------------------

def dB2pwr(rasterdB):
    '''
    Convert from dB to power
    '''
    rasterPwr = np.power(10.,rasterdB/10.)
    return rasterPwr
    
#-----------------------------------------------------------------------

def dB2Amp(rasterdB):
    '''
    Convert from dB to Amp
    '''
    rasterAmp=np.power(10.,rasterdB/20.)
    return rasterAmp
    
#-----------------------------------------------------------------------

def pwr2amp(rasterPwr):
    '''
    Convert from power to amplitude
    '''
    rasterAmp=np.sqrt(rasterPwr)
    return rasterAmp
    
#-----------------------------------------------------------------------

def rescale(raster):
    '''
    Generate an 8-bit scaled dB image 
    '''
    vmin = np.min(raster)
    vmax = np.max(raster)
    rasterRes = ((255-0)*((raster-vmin)/(vmax-vmin)))+0
    rasterRes = rasterRes.astype(np.uint8)
    return rasterRes
    
#-----------------------------------------------------------------------

def rescale2(rasterDN):
    '''
    Generate an 8-bit scaled dB image
    (non funziona)
    '''
    mask=rasterDN==0
    CF=np.power(10.,-8.3)
    rasterPwr=np.ma.array(np.power(rasterDN,2.)*CF,mask=mask,dtype=np.float32)
    rasterDB=(10.*np.ma.log10(rasterPwr)+31)/0.15
    print("Range min ", np.min(rasterDB), " max ", np.max(rasterDB))
    rasterDB[rasterDB<1.]=1.
    rasterDB[rasterDB>255.]=255.
    rasterDB=rasterDB.astype(np.uint8)
    rasterDB=rasterDB.filled(0)
    return rasterDB
    
#-----------------------------------------------------------------------

def Power(rasterDN):
    '''
    Convert DN to Power
    '''
    mask=rasterDN==0
    CF=np.power(10.,-8.3)
    rasterPwr=np.ma.array(np.power(rasterDN,2.)*CF,mask=mask,dtype=np.float32)
    return rasterPwr

#-----------------------------------------------------------------------
