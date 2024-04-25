"""Base Bubble Entropy function."""
import numpy as np

def BubbEn(Sig, m=2, tau=1, Logx=np.exp(1)):
    """BubbEn  estimates the bubble entropy of a univariate data sequence.
 
    .. code-block:: python
    
        Bubb, H = BubbEn(Sig)
    
    Returns the bubble entropy (``Bubb``) and the conditional Rényi entropy (``H``)
    estimate from the data sequence (``Sig``) using the default parameters: 
    embedding dimension = 2, time delay = 1, logarithm = natural 
  
    .. code-block:: python
        
        Bubb, H = BubbEn(Sig, keyword = value, ...)
    
    Returns the bubble entropy (``Bubb``) estimated from the data sequence (``Sig``)  
    using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
            BubbEn returns estimates for each dimension [2, ..., ``m``]   
        :tau:   - Time Delay, a positive integer
        :Logx:  - Logarithm base, a positive scalar
 
    :See also:
        ``PhasEn``, ``MSEn``

    :References:
        [1] George Manis, M.D. Aktaruzzaman and Roberto Sassi,
            "Bubble entropy: An entropy almost free of parameters."
            IEEE Transactions on Biomedical Engineering
            64.11 (2017): 2711-2718.
    
    """  

    Sig = np.squeeze(Sig)
    N = Sig.shape[0]
    
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
                
    Sx = np.zeros((N,m+1))
    H = np.zeros(m+1)
    Sx[:,0] = Sig    
    for k in range(2,m+2):
        
        Sx[0:N-(k-1)*tau,k-1] = Sig[(k-1)*tau:N]
        temp = np.copy(Sx[0:N-(k-1)*tau,0:k])
        Swapx, _ = BubbSort(temp)
        _, Locs = np.unique(Swapx, return_counts=True)
        p = Locs/(N-(k-1)*tau)
        H[k-1] = -np.log(np.sum(p**2))/np.log(Logx)
        if np.round(np.sum(p)) != 1:
            raise Exception('Potential error in detected swap number')
        del Swapx, p, Locs, temp
         
    with np.errstate(divide='ignore', invalid='ignore'):
        BE = np.diff(H)/((np.log(np.arange(2,m+2)/np.arange(m)))/np.log(Logx))
    
    BE = BE[1:]
    return BE, H

def BubbSort(Data):
    x, N2 = np.shape(Data)
    swaps = np.zeros(x)
    for y in range(x):
        for t in range(N2-1):
            for kk in range(N2-t-1):
                if Data[y,kk] > Data[y,kk+1]:
                    Data[y,kk], Data[y,kk+1] = Data[y,kk+1], Data[y,kk]
                    swaps[y] += 1
    bsorted = Data
    return swaps, bsorted   
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