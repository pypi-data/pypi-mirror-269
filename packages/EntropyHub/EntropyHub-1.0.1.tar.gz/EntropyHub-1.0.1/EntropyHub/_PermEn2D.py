"""Base Bidimensional Permutation Entropy function."""
import numpy as np   

def PermEn2D(Mat, m=None, tau=1, Norm=True, Logx=np.exp(1), Lock=True):
    """PermEn2D  Estimates the bidimensional permutation entropy of a data matrix.

    .. code-block:: python
    
        Perm2D = PermEn2D(Mat) 
            
    Returns the bidimensional permutation entropy estimate (``Perm2D``) estimated for 
    the data matrix (``Mat``) using the default parameters: time delay = 1,
    logarithm = natural, template matrix size = [floor(H/10) floor(W/10)]  
    (where H and W represent the height (rows) and width (columns) of the data matrix ``Mat``) 
    ** The minimum number of rows and columns of ``Mat`` must be > 10.
 
     .. code-block:: python
     
         Perm2D = PermEn2D(Mat, keyword = value, ...)
    
    Returns the bidimensional permutation entropy (``Perm2D``) estimates for the data
    matrix (``Mat``) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer scalar (for sub-matrix with same height and width) or a two-element tuple of integers (height, width) with a minimum value > 1. (default: [floor(H/10) floor(W/10)])
        :tau:   - Time Delay, a positive integer > 1   (default: 1)
        :Norm:  - Normalization of the PermEn2D value by maximum Shannon entropy (Smax = log((mx*my)!)         [default: true]
        :Logx:  - Logarithm base, a positive scalar    (default: natural)        
        :Lock:  - By default, ``PermEn2D`` only permits matrices with a maximum size of 128 x 128 to prevent RAM overload. 
                    e.g. For ``Mat`` = [200 x 200], ``m = 3``, and ``tau = 1``, ``PermEn2D`` 
                    creates a vector of 753049836 elements. To enable matrices
                    greater than [128 x 128] elements, set ``'Lock' = false``. (default: true)
                    ``CAUTION: unlocking the permitted matrix size may cause memory``
                    ``errors that could lead your Python IDE to crash.``
                    
        
    **NOTE**: 
	     ``The original bidimensional permutation entropy algorithms [1][2]``
	     ``do not account for equal-valued elements of the embedding matrices.``
             To overcome this, PermEn2D uses the lowest common rank for
             such instances. For example, given an embedding matrix A where,
             A = [3.4  5.5  7.3]         
                 [2.1  6    9.9]       
                 [7.3  1.1  2.1]        
             would normally be mapped to an ordinal pattern like so,      
             [3.4  5.5  7.3  2.1  6  9.9  7.3  1.1  2.1] =>
             [ 8    4    9    1   2   5    3    7    6 ]
             However, indices 4 & 9, and 3 & 7 have the same values, 2.1
             and 7.3 respectively. Instead, PermEn2D uses the ordinal pattern
             [ 8    4    4    1   2   5    3    3    6 ]
             where the lowest rank (4 & 3) are used instead (of 9 & 7). 
             Therefore, the number of possible permutations is no longer 
             (mx*my)!, but (mx*my)^(mx*my). Here, the PermEn2D value is 
             normalized by the maximum Shannon entropy (Smax = log((mx*my)!) 
             ``assuming that no equal values are found in the permutation
             motif matrices``, as presented in [1].

    :See also:
        ``SampEn2D``, ``FuzzEn2D``, ``DistEn2D``, ``DispEn2D``, ``EspEn2D``
     
    
    :References:
        [1] Haroldo Ribeiro et al.,
            "Complexity-Entropy Causality Plane as a Complexity Measure 
            for Two-Dimensional Patterns"
            PLoS ONE (2012), 7(8):e40689, 
    
        [2] Luciano Zunino and Haroldo Ribeiro,
             "Discriminating image textures with the multiscale
             two-dimensional complexity-entropy causality plane"
             Chaos, Solitons and Fractals,  91:679-688 (2016)
    
        [3] Matthew Flood and Bernd Grimm,
             "EntropyHub: An Open-source Toolkit for Entropic Time Series Analysis"
             PLoS ONE (2021) 16(11): e0259448.
                                 
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
    assert isinstance(Norm,bool), "Norm: must be a boolean"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate PermEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])       
        
    NL = NL - (mL-1)*tau
    NW = NW - (mW-1)*tau
    
    Temp = Mat[:(mL-1)*tau+1:tau,:(mW-1)*tau+1:tau]
    Sord = np.sort(Temp.flatten('F'))
    Dict = np.argsort(Temp.flatten('F'),kind='stable')
    if np.any(np.diff(Sord)==0):
        for x in np.where(np.diff(Sord)==0)[0]+1:
            Dict[x] = Dict[x-1]  
 
    Counter = 0
    Dict = np.expand_dims(Dict,axis=0)
    
    for k in range(NL):        
        for n in range(NW):            
            Temp = Mat[k:(mL-1)*tau+k+1:tau,n:(mW-1)*tau+n+1:tau]
            Sord = np.sort(Temp.flatten('F'))
            Dx = np.argsort(Temp.flatten('F'),kind='stable')
            
            if np.any(np.diff(Sord)==0):
                for x in np.where(np.diff(Sord)==0)[0]+1:
                    Dx[x] = Dx[x-1] 
                    
            if np.any(~np.any(Dict - Dx, axis=1)):
                Counter += ~np.any(Dict - Dx, axis=1)*1
                
            else:
                Dict = np.vstack((Dict, Dx))
                Counter = np.hstack((Counter, 1))
                
    if np.sum(Counter) != NL*NW:
        print('Warning: Potential error with permutation comparisons.')        

    Pi = Counter/sum(Counter) 
    Perm2D = -np.sum(Pi*np.log(Pi)/np.log(Logx))
                  
    if Norm:
        Perm2D = Perm2D/(np.log(float(np.math.factorial(mL*mW)))/np.log(Logx))
                     
    return Perm2D

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