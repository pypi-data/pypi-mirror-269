"""Base corrected Conditional Entropy function."""
import numpy as np

def CondEn(Sig, m=2, tau=1, c=6, Logx=np.exp(1), Norm=False):
    """CondEn  estimates the corrected conditional entropy of a univariate data sequence.

    .. code-block:: python
        
        Cond, SEw, SEz = CondEn(Sig) 
        
    Returns the corrected conditional entropy estimates (``Cond``) and the
    corresponding Shannon entropies (``m``: ``SEw``, ``m+1``: ``SEz``) for ``m`` = [1,2] 
    estimated from the data sequence (``Sig``) using the default parameters:
    embedding dimension = 2, time delay = 1, symbols = 6, logarithm = natural, normalisation = False
    Note: ``CondEn(m=1)`` returns the Shannon entropy of ``Sig``.
    
    .. code-block::
        
        Cond, SEw, SEz = CondEn(Sig, keyword = value, ...)
        
    Returns the corrected conditional entropy estimates (Cond) from the data
    sequence (Sig) using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
        :tau:   - Time Delay, a positive integer
        :c:     - Number of symbols, an integer > 1
        :Logx:  - Logarithm base, a positive scalar 
        :Norm:  - Normalisation of ``Cond`` value, a boolean:
            * ``False``  no normalisation - default
            * ``True``   normalises w.r.t Shannon entropy of data sequence ``Sig``.  
 
    :See also:
        ``XCondEn``, ``MSEn``, ``PermEn``, ``DistEn``, ``XPermEn``
    
    :References:
        [1] Alberto Porta, et al.,
            "Measuring regularity by means of a corrected conditional
            entropy in sympathetic outflow." 
            Biological cybernetics 
            78.1 (1998): 71-78.
    """

    Sig = np.squeeze(Sig)    
        
    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(c,int) and (c > 1), "c:   must be an integer > 1"
    assert isinstance(Logx,(int,float)) and Logx > 0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"
        
    Sig = (Sig-np.mean(Sig))/np.std(Sig)
    # Edges = np.linspace(min(Sig),max(Sig),c+1)
    Edges = np.arange(min(Sig),max(Sig),np.ptp(Sig)/c)
    Sx = np.digitize(Sig,Edges)
    # Sx[Sx==max(Sx)] = c
    N = Sx.shape[0]
    SEw = np.zeros(m-1)
    SEz = np.zeros(m-1)
    Prcm = np.zeros(m-1)
    Xi = np.zeros((N,m))
    Xi[:,-1] = Sx    
    for k in range(1,m):    #1:m-1
        Nx = N-(k*tau)
        Xi[:Nx,-(k+1)] = Sx[k*tau:]
        Wi = np.inner(c**np.arange(k-1,-1,-1),Xi[:Nx,-k:])
        Zi = np.inner(c**np.arange(k,-1,-1), Xi[:Nx,-(k+1):])
        Pw, _ = np.histogram(Wi,np.arange(min(Wi)-.5,max(Wi)+1.5))
        Pz, _ = np.histogram(Zi,np.arange(min(Zi)-.5,max(Zi)+1.5))
        Prcm[k-1] = sum(Pw==1)/Nx
        
        if sum(Pw)!=Nx or sum(Pz)!=Nx:
            print('Warning: Potential error estimating probabilities.')
        Pw = Pw[Pw!=0]; Pw = Pw/N
        Pz = Pz[Pz!=0]; Pz = Pz/N
        SEw[k-1] = -sum(Pw*np.log(Pw)/np.log(Logx))
        SEz[k-1] = -sum(Pz*np.log(Pz)/np.log(Logx))
        del Pw, Pz, Wi, Zi
        
    Temp, _ = np.histogram(Sx,c)
    Temp = Temp[Temp!=0]/N
    S1 = -sum(Temp*np.log(Temp)/np.log(Logx))
    Cond = SEz - SEw + Prcm*S1
    Cond = np.hstack((S1, Cond))
    if Norm:
        Cond = Cond/S1
    
    return Cond, SEw, SEz
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