"""Base Bidimensional Dispersion Entropy function."""
import numpy as np
from scipy.special import ndtr
from scipy.cluster.vq import kmeans2

def DispEn2D(Mat, m=None, tau=1, c=3, Typex='NCDF', Logx=np.exp(1), Norm=False, Lock=True):
    """DispEn2D  Estimates the bidimensional dispersion entropy of a data matrix.
    
    .. code-block:: python
    
        Disp2D, RDE = DispEn2D(Mat) 
        
    Returns the bidimensional dispersion entropy estimate (``Disp2D``) and 
    reverse bidimensional dispersion entropy (``RDE``) estimated for the data 
    matrix (``Mat``) using the default parameters:  time delay = 1, symbols = 3,
    logarithm = natural, data transform = normalised cumulative density function (ncdf)
    matrix template size = [floor(H/10) floor(W/10)]  
    (where H and W represent the height (rows) and width (columns) of the
    data matrix ``Mat``) 
    * The minimum number of rows and columns of Mat must be > 10.
 
    .. code-block:: python
    
        Disp2D, RDE = DistEn2D(Mat, keyword = value, ...)
    
    Returns the bidimensional distribution entropy (``Dist2D``) estimate for 
    the data matrix (Mat) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer scalar 
                (for submatrix with same height and width) or a two-element vector of
                integers [height, width] with a minimum value > 1.
                (default: [floor(H/10) floor(W/10)])
                
        :tau:   - Time Delay, a positive integer  (default: 1)
        :c:     - Number of symbols, an integer > 1
        :Typex: - Typex of data-to-symbol mapping, one of the following strings: 
                {``'linear'``, ``'kmeans'``, ``'ncdf'``, ``'equal'``}
                See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info on these transforms.                   
       
        :Logx:  - Logarithm base, a positive scalar
        :Norm:  - Normalisation of ``Disp2D`` and ``RDE`` values, a boolean:
            	* ``False``  no normalisation - default
           	* ``True``  normalises w.r.t # possible vector permutations (c^m).
              
        :Lock:  - By default, ``DispEn2D`` only permits matrices with a maximum size of 128 x 128 to prevent RAM overload. 
                e.g. For ``Mat`` = [200 x 200], ``m`` = 3, and ``tau`` = 1, ``DispEn2D`` 
                creates a vector of 753049836 elements. To enable matrices greater than [128 x 128] elements, set ``Lock = False`` (default: True)
              
                ``CAUTION: unlocking the permitted matrix size may cause memory``
                ``errors that could lead your Python IDE to crash.``
    
    :See also:
        ``DispEn``, ``SampEn2D``, ``FuzzEn2D``, ``DistEn2D``
    
    :References:
        [1] Hamed Azami, et al.,
            "Two-dimensional dispersion entropy: An information-theoretic 
            method for irregularity analysis of images."
            Signal Processing: Image Communication, 
            75 (2019): 178-187.
    
    """
        
    Mat = np.squeeze(Mat)
    NL,NW = Mat.shape    
    if m is None:  m = np.array(Mat.shape)//10
    if Logx == 0:  Logx = np.exp(1)
           
    assert Mat.ndim==2 and min(Mat.shape)>10 , \
    "Mat:   must be a 2D numpy array with height & width > 10"
    assert (isinstance(m,int) and m>1) \
        or (isinstance(m, (np.ndarray,tuple)) and len(m)==2 and min(m)>1), \
    "m:     must be an integer > 1, or a 2 element tuple of integers > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"     
    assert isinstance(c,int) and (c > 1), "c:     must be an integer > 1"
    assert Typex.lower() in ['linear','kmeans','ncdf','equal'], \
            "Typex:    must be one of the following strings - \
            'linear', 'kmeans', 'ncdf', 'equal'"      
    assert isinstance(Norm,bool), "Norm:     must be boolean (true or false)"   
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate DispEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])   
        
    if Typex.lower() == 'linear':
        Zi = np.digitize(Mat,np.arange(np.min(Mat),np.max(Mat),np.ptp(Mat)/c))
        
    elif Typex.lower() == 'kmeans':        
        Clux, Zx = kmeans2(Mat.flatten(), c, iter=200)
        Zx += 1;  xx = np.argsort(Clux) + 1;     Zi = np.zeros(Mat.size);
        for k in range(1,c+1):
            Zi[Zx==xx[k-1]] = k;
        Zi = np.reshape(Zi,Mat.shape)
        
    elif Typex.lower() == 'ncdf':  
        Zx = ndtr((Mat-np.mean(Mat))/np.std(Mat))
        Zi = np.digitize(Zx,np.arange(0,1,1/c))  
        
        del Zx
                        
    elif Typex.lower() == 'equal':
        ix = np.argsort(Mat.flatten(),kind='mergesort')
        xx = np.round(np.arange(0,2*Mat.size,Mat.size/c)).astype(int)
        Zi = np.zeros(Mat.size)
        for k in range(c):
            Zi[ix[xx[k]:xx[k+1]]] = k+1 
            
        Zi = np.reshape(Zi, Mat.shape)
        del ix, xx, k                   
              
    NL = NL - (mL - 1)*tau
    NW = NW - (mW - 1)*tau
    X = np.zeros((NL*NW,mL*mW))
    p = 0
    for k in range(0,NL):        
        for n in range(0,NW):
              X[p,:] = Zi[k:mL*tau+k:tau,n:mW*tau+n:tau].flatten('F')
              p += 1              
    if p != NL*NW:
        print('Warning: Potential error with submatrix division.')        
        
    T  = np.unique(X,axis=0)
    Nx = T.shape[0]
    Counter = np.zeros(Nx)       
    for n in range(Nx):
        Counter[n] = sum(np.any(X - T[n,:],axis=1)==False)

    Ppi = Counter[Counter!= 0]/X.shape[0]
    if np.longdouble(c)**(mL*mW) > np.longdouble(10)**16:
        raise Exception("""RDE cannot be estimated with c = %d and a submatrix of size %d x %d.
        Required floating point precision exceeds 10^16.
        Consider reducing the template submatrix size (m) or the number of symbols (c).""" %(c, mL, mW))
    
    # RDE = sum(Ppi**2) - (1/Nx)
    RDE = sum((Ppi - (1/(c**(mL*mW))))**2); 
    Disp2D = -sum(Ppi*np.log(Ppi)/np.log(Logx))    
    
    if round(sum(Ppi)) != 1:
        print('Potential error calculating probabilities')    
        
    if Norm:
        Disp2D = Disp2D/(np.log(c**(mL*mW))/np.log(Logx))
        RDE = RDE/(1 - (1/(c**(mL*mW))))     
        
    return Disp2D, RDE

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

    
    
    
