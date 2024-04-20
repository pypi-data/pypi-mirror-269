"""Base Bidimensional Espinosa Entropy function."""
import numpy as np    

def EspEn2D(Mat, m=None, tau=1, r=20, ps=0.7, Logx=np.exp(1), Lock=True):
    """EspEn2D  Estimates the bidimensional Espinosa entropy of a data matrix.

    .. code-block:: python
    
        Esp2D = EspEn2D(Mat) 
        
    Returns the bidimensional Espinosa entropy estimate (``Esp2D``) 
    estimated for the data matrix (``Mat``) using the default parameters: 
    time delay = 1, tolerance threshold = 20, percentage similarity = 0.7
    logarithm = natural, matrix template size = [floor(H/10) floor(W/10)]  
    (where H and W represent the height (rows) and width (columns) of 
    the data matrix ``Mat``) 
    ** The minimum number of rows and columns of ``Mat`` must be > 10.
 
     .. code-block:: python
     
         Esp2D = EspEn2D(Mat, keyword = value, ...)
    
    Returns the bidimensional Espinosa entropy (``Esp2D``) estimates for the data
    matrix (``Mat``) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer scalar (for sub-matrix with same height and width) or a two-element tuple of integers (height, width) with a minimum value > 1. (default: [floor(H/10) floor(W/10)])
        :tau:   - Time Delay, a positive integer > 1   (default: 1)
        :r:     - Tolerance Threshold, a positive scalar   (default: 20)
        :ps:    - Percentage similarity, a scalar in range [0 1] (default: 0.7)        
        :Logx:  - Logarithm base, a positive scalar    (default: natural)        
        :Lock:  - By default, ``EspEn2D`` only permits matrices with a maximum  size of 128 x 128 to prevent RAM overload. 
              e.g. For ``Mat`` = [200 x 200], ``m`` = 3, and ``tau`` = 1, ``EspEn2D`` 
              creates a vector of 753049836 elements. To enable matrices greater than [128 x 128] elements, set ``Lock = False`` (default: True)
              ``CAUTION: unlocking the permitted matrix size may cause memory``
              ``errors that could lead your Python IDE to crash.``
    
    :See also:
        ``SampEn2D``, ``FuzzEn2D``, ``DistEn2D``, ``DispEn2D``
    
    :References:
        [1] Ricardo Espinosa, et al.,
          "Two-dimensional EspEn: A New Approach to Analyze Image Texture 
          by Irregularity." 
          Entropy,
          23:1261 (2021)
                                 
    """
            
    Mat = np.squeeze(Mat)
    NL,NW = Mat.shape    
    if m is None:
        m = np.array(Mat.shape)//10
           
    assert Mat.ndim==2 and min(Mat.shape)>10 , \
    "Mat:   must be a 2D numpy array with height & width > 10"
    assert (isinstance(m,int) and m>1) or (isinstance(m, (np.ndarray,tuple))  
                                           and len(m)==2 and min(m)>1), \
    "m:     must be an integer > 1, or a 2 element tuple of integers > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>0, "r:     must be a positive value"
    assert isinstance(ps,float) and ps>=0 and ps<=1, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate EspEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])       
        
    NL = NL - (mL-1)*tau
    NW = NW - (mW-1)*tau
    X = np.zeros((NL*NW,mL,mW))
    p = 0
    for k in range(NL):        
        for n in range(NW):
            X[p,:,:] = Mat[k:(mL*tau)+k:tau,n:(mW*tau)+n:tau]
            p += 1              
            
    if p != NL*NW:
        print('Warning: Potential error with submatrix division.')        
    Ny = int(p*(p-1)/2)
    if Ny > 300000000:
        print('Warning: Number of pairwise distance calculations is ' + str(Ny))
    
    Cij = -np.ones((p-1,p-1))
    for k in range(p-1):
        Temp = abs(X[k+1:,:,:] - X[k,:,:]) <= r
        Cij[:p-(k+1),k] = np.sum(Temp,axis=(1,2))
     
    Dm = np.sum((Cij/(mL*mW))>=ps)/(p*(p-1)/2)
    Esp2D = -np.log(Dm)/np.log(Logx)
    return Esp2D

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