
# https://ecocodespace.wordpress.com/2012/07/06/upper-envelope-fitting-to-ndvi-time-series/

from scipy.optimize import leastsq
from numpy import *
import numpy
import pylab
from copy import copy
 
######################################################### FUNCTIONS
 
# Logistic function, returns predicted Y given parameters p
def logFun(p,X):
    a,b,r1,s1,d1,e1=p
    pY=a+(b*((1/(1+numpy.exp(r1*(s1-X))))+(1/(1+numpy.exp(d1*(e1-X))))-1))
    return pY
 
# Error function, returns residuals given X,Y and parameters p
def logErr(p,X,Y):
    pY=logFun(p,X)
    eY=(Y-pY)
    return eY
 
# Upper-envelope fitting algorithm. Moves envelope up 'numTimes' by 
# sequentially filtering Y and refitting 'logFun'
def upperEnvFit(X,Y,p,numTimes):
    stP=p
    for i in range(numTimes):
        # Fit model, get new parameters (p is revaluated at every iteration)
        p,flag=leastsq(logErr,stP,args=(X,Y),maxfev=10000)
        # Predict new Y values using new parameters
        predY=logFun(p,X)
        # Set values which are lower than Y to predicted Y
        Y[Y<predY]=predY[Y<predY]
    # After updating 'numTimes' times, produce new estimates
    finalY=logFun(p,X)
    return [p,finalY]
 
######################################################### PROCESS DATA
 
# Initial guess for starting parameters, will need to be tweaked given 
# shape of data
stVars=['Minimum NDVI','Max-Min NDVI','Rate of increase', \
'Start of season','Rate of decline','End of season']
p=[0.3,0.6,0.2,100,-0.08,275]
 
# Example X vector (Dates)
X=array(range(365))+1
 
# Get Y given parameters 'p'
Y=logFun(p,X)
pylab.plot(X,Y)
 
# Add noise to Y
noise=numpy.random.normal(0.0, 0.02, size=(len(Y)))
nY=Y+noise
 
# Create some gaps
gY=copy(nY)
gY[noise<-0.02]=0
pylab.plot(X,gY)
 
### Run gap filling
# ...number of times filtering is to be done
numTimes=4
newP,fY=upperEnvFit(X,gY,p,numTimes)
pylab.plot(X,fY)   # Filled time series
 
pylab.show()
 
for i in range(len(p)):
    print stVars[i],'Original:',p[i],'Retrieved:',newP[i]
