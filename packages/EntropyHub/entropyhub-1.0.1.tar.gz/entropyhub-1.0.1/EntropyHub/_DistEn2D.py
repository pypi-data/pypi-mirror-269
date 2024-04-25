"""Base Bidimensional Distribution Entropy function."""
import numpy as np
from scipy.stats import skew

def DistEn2D(Mat, m=None, tau=1, Bins='Sturges', Logx=2, Norm=2, Lock=True):
    """DistEn2D  Estimates the bidimensional distribution entropy of a data matrix.
    
    .. code-block:: python
    
        Dist2D = DistEn2D(Mat) 
        
    Returns the bidimensional distribution entropy estimate (``Dist2D``)
    estimated for the data matrix (``Mat``) using the default parameters:
    time delay = 1, binning method = 'sturges', logarithm = natural, 
    matrix template size = [floor(H/10) floor(W/10)] (where H and W represent
    the height (rows) and width (columns) of the data matrix ``Mat``) 
    * The minimum dimension size of ``Mat`` must be > 10.
 
    .. code-block:: python
    
        Dist2D = DistEn2D(Mat, keyword = value, ...)
    
    Returns the bidimensional distribution entropy (``Dist2D``) estimate for 
    the data matrix (Mat) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer scalar (for sub-matrix with same height and width) or a two-element tuple of integers [height, width] with a minimum value > 1. (default: [floor(H/10) floor(W/10)])
        :tau:   - Time Delay, a positive integer  (default: 1)
        :Bins:  - Histogram bin selection method for distance distribution, one of the following:
            * an integer > 1 indicating the number of bins, 
            * or one of the following strings {``'sturges'``, ``'sqrt'``, ``'rice'``, ``'doanes'``} [default: 'sturges']
              
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of Dist2D value, one of the following integers:
            * [0]  no normalisation.
            * [1]  normalises values of data matrix (Mat) to range [0 1].
            * [2]  normalises values of data matrix (Mat) to range [0 1], and normalises the distribution entropy value (``Dist2D``) w.r.t the number of histogram bins.  [default]
            * [3]  normalises the distribution entropy value (``Dist2D``) w.r.t the number of histogram bins, without normalising  data matrix values.
        :Lock:  - By default, ``DistEn2D`` only permits matrices with a maximum size of 128 x 128 to prevent RAM overload. 
              e.g. For ``Mat`` = [200 x 200], ``m`` = 3, and ``tau`` = 1, ``DistEn2D`` 
              creates a vector of 753049836 elements. To enable matrices greater than [128 x 128] elements, set ``Lock = False`` (default: True)
              
              ``CAUTION: unlocking the permitted matrix size may cause memory``
              ``errors that could lead your Python IDE to crash.``
    
    :See also:
        ``DistEn``, ``XDistEn``, ``SampEn2D``, ``FuzzEn2D``, ``MSEn``
    
    :References:
        [1] Hamed Azami, Javier Escudero and Anne Humeau-Heurtier,
            "Bidimensional distribution entropy to analyze the irregularity
            of small-sized textures."
            IEEE Signal Processing Letters 
            24.9 (2017): 1338-1342.
    
    """
        
    Mat = np.squeeze(Mat)
    NL,NW = Mat.shape    
    if m is None:
        m = np.array(Mat.shape)//10
    if Logx == 0:
        Logx = np.exp(1)
           
    assert Mat.ndim==2 and min(Mat.shape)>10 , \
    "Mat:   must be a 2D numpy array with height & width > 10"
    assert (isinstance(m,int) and m>1) \
        or (isinstance(m, (np.ndarray,tuple)) and len(m)==2 and min(m)>1), \
    "m:     must be an integer > 1, or a 2 element tuple of integers > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"     
    assert (isinstance(Bins,int) and Bins > 1) \
        or (Bins.lower() in ['sturges','sqrt','rice','doanes']), \
        "Bins:    an integer > 1, or can be one of the following strings - \
        'sturges', 'sqrt', 'rice', 'doanes'"
    assert isinstance(Norm,int) and np.isin(Norm,np.arange(4)), "Norm:     must be integer in range [0 4]"   
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate DistEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])   
           
    if Norm == 1 or Norm == 2:
        Mat = (Mat - np.min(Mat))/np.ptp(Mat[:])
   
    NL = NL - (mL - 1)*tau
    NW = NW - (mW - 1)*tau
    X = np.zeros((NL*NW,mL,mW))
    p = 0
    for k in range(0,NL):        
        for n in range(0,NW):
              X[p,:,:] = Mat[k:mL*tau+k:tau,n:mW*tau+n:tau]
              p += 1              
    if p != NL*NW:
        print('Warning: Potential error with submatrix division.')        
    Ny = int(p*(p-1)/2)
    if Ny > 300000000:
        print('Warning: Number of pairwise distance calculations is ' + str(Ny))
    
    Y = np.zeros(Ny)
    for k in range(1,p):
        Ix = (int((k-1)*(p - k/2)), int(k*(p-((k+1)/2))))        
        Y[Ix[0]:Ix[1]] = np.max(abs(X[k:,:,:] - X[k-1,:,:]),axis=(1,2))
     
    if isinstance(Bins, str):
        if Bins.lower() == 'sturges':
            Bx = np.ceil(np.log2(Ny) + 1)
        elif Bins.lower() == 'rice':
            Bx = np.ceil(2*(Ny**(1/3)))
        elif Bins.lower() == 'sqrt':
            Bx = np.ceil(np.sqrt(Ny))
        elif Bins.lower()== 'doanes':
            sigma = np.sqrt(6*(Ny-2)/((Ny+1)*(Ny+3)))
            Bx = np.ceil(1+np.log2(Ny)+np.log2(1+abs(skew(Y)/sigma)))
        else:
            raise Exception('Please enter a valid binning method')               
    else:
        Bx = Bins
        
    By = np.linspace(min(Y),max(Y),int(Bx+1))
    Ppi,_ = np.histogram(Y,By)        
    Ppi = Ppi/Ny
    if round(sum(Ppi),6) != 1:
        print('Warning: Potential error estimating probabilities (p = ' +str(np.sum(Ppi))+ '.')
        Ppi = Ppi[Ppi!=0]
    elif any(Ppi==0):
        print('Note: '+str(sum(Ppi==0))+'/'+str(len(Ppi))+' bins were empty')
        Ppi = Ppi[Ppi!=0]
           
    Dist2D = -sum(Ppi*np.log(Ppi)/np.log(Logx))
    if Norm >= 2:
        Dist2D = Dist2D/(np.log(Bx)/np.log(Logx))
      
    return Dist2D

"""
    Copyright 2024 Matthew W. Flood, EntropyHub
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    For Terms of Use see https://github.com/MattWillFlood/EntropyHub
"""