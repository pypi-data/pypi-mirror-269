"""Base Slope Entropy function."""
import numpy as np

def SlopEn(Sig, m=2, tau=1, Lvls=(5,45), Logx=2, Norm=True):
    """SlopEn  estimates the slope entropy of a univariate data sequence.

    .. code-block:: python
    
        Slop = SlopEn(Sig) 
        
    Returns the slope entropy (``Slop``) of the data sequence (``Sig``) for embedding 
    dimensions [2, ..., ``m``] using the default parameters:  embedding dimension = 2, 
    time delay = 1, angular thresholds = [5 45],  logarithm = base 2 
  
    .. code-block:: python
    
        [Slop] = SlopEn(Sig, keyword = value, ...)
        
    Returns the slope entropy (``Slop``) estimates of the data sequence (``Sig``)  
    using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
              SlopEn returns estimates for each dimension [2,..., ``m``]
        :tau:   - Time Delay, a positive integer
        :Lvls:  - Angular thresolds, a vector of monotonically increasing  values in the range [0 90] degrees.
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log)
        :Norm:  - Normalisation of ``SlopEn`` value, one of the following integers:
            * [False]  no normalisation
            * [True]   normalises w.r.t. the number of patterns found (default)
 
    :See also:
        ``PhasEn``, ``GridEn``, ``MSEn``, ``CoSiEn``, ``SampEn``, ``ApEn``
  
    :References:
        [1] David Cuesta-Frau,
            "Slope Entropy: A New Time Series Complexity Estimator Based on
            Both Symbolic Patterns and Amplitude Information." 
            Entropy 
            21.12 (2019): 1167.
    """
    
    Sig = np.squeeze(Sig)
    if Logx == 0:
        Logx = np.exp(1)
    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"  
    assert isinstance(Lvls,(tuple,np.ndarray)) and len(Lvls)>1 and min(np.diff(Lvls))>0 \
        and  min(Lvls)>0 and max(Lvls)<=90, "Lvls:  must be a tuple/numpy \
        vector with multiple monotonically increasing values in range [0 90]"
               
    m = m-1
    Tx = np.degrees(np.arctan(Sig[tau:] - Sig[:-tau]))
    N = Tx.shape[0]
    Sx = np.zeros((N,m))
    Symbx = np.zeros(N) #np.shape(Tx))
    Slop = np.zeros(m)    
    for q in range(1,len(Lvls)):        
        Symbx[np.logical_and(Tx<= Lvls[q], Tx> Lvls[q-1])] = q
        Symbx[np.logical_and(Tx>=-Lvls[q], Tx<-Lvls[q-1])] = -q
        
        if q == len(Lvls)-1:
            Symbx[Tx> Lvls[q]] = q+1
            Symbx[Tx<-Lvls[q]] = -(q+1)
               
    for k in range(m):
        Sx[:N-k,k] = Symbx[k:N]
        _,Locs = np.unique(Sx[:N-k,:k+1],axis=0,return_counts=True)
        
        if Norm:
            p = Locs/(N-k)        
            if np.round(np.sum(p))!= 1:
                print('WARNING: Potential Error: Some permutations not accounted for!')
        else:
            p = Locs/len(Locs)
        
        Slop[k] = -np.sum(p*np.log(p)/np.log(Logx))
        del Locs, p
    
    return Slop
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