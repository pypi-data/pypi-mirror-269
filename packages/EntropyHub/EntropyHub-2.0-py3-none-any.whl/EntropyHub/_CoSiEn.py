"""Base Cosine Similarity Entropy function."""
import numpy as np 

def CoSiEn(Sig,  m=2, tau=1, r=0.1, Logx=2, Norm=0):
    """CoSiEn  estimates the cosine similarity entropy of a univariate data sequence.
    
    .. code-block:: python
        
        CoSi, Bm = CoSiEn(Sig) 
        
    Returns the cosine similarity entropy (``CoSi``) and the corresponding
    global probabilities (``Bm``) estimated from the data sequence (``Sig``) using the
    default parameters:   embedding dimension = 2, time delay = 1, 
    angular threshold = .1,  logarithm = base 2,

    .. code-block:: python
        
        CoSi, Bm = CoSiEn(Sig, keyword = value, ...)
        
    Returns the cosine similarity entropy (``CoSi``) estimated from the data
    sequence (``Sig``) using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
        :tau:   - Time Delay, a positive integer
        :r:     - Angular threshold, a value in range [0 < ``r`` < 1]
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of ``Sig``, one of the following integers:
            
                  0.  no normalisation - default
                  1.  normalises ``Sig`` by removing median(``Sig``)
                  2.  normalises ``Sig`` by removing mean(``Sig``)
                  3.  normalises ``Sig`` w.r.t. SD(``Sig``)
                  4.  normalises ``Sig`` values to range [-1 1]

    :See also:
        ``PhasEn``, ``SlopEn``, ``GridEn``, ``MSEn``, ``hMSEn``
    
    :References:
        [1] Theerasak Chanwimalueang and Danilo Mandic,
            "Cosine similarity entropy: Self-correlation-based complexity
            analysis of dynamical systems."
            Entropy 
            19.12 (2017): 652.
            
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]  
    if Logx == 0:
        Logx = np.exp(1)
        
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r, (int,float)) and r >= 0 and r <= 1, "r:    must be a value in range [0 1]"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,int) and np.isin(Norm, np.arange(5)), "Norm:     must be an integer in range [0 4]"
                   
    if Norm == 1:
        Xi = Sig - np.median(Sig)
    elif Norm == 2:
        Xi = Sig - np.mean(Sig)
    elif Norm == 3:
        Xi = (Sig - np.mean(Sig))/np.std(Sig)
    elif Norm == 4:
        Xi = (2*(Sig - min(Sig))/np.ptp(Sig)) - 1
    else:
        Xi = Sig        
    
    Nx = N - (m-1)*tau
    Zm = np.zeros((Nx,m))
    for n in range(m):
        Zm[:,n] = Xi[n*tau:Nx+(n*tau)]
        
    Num = np.inner(Zm,Zm)
    #Mag = np.linalg.norm(Zm, axis=1) # Dont know which is faster...
    Mag = np.sqrt(np.diag(Num))
    Den = np.outer(Mag, Mag)
                
    AngDis = np.arccos(np.triu(Num/Den,1))/np.pi    
    if np.max(np.imag(AngDis)) < 10**-6:
        Bm = np.sum(np.triu(np.round(AngDis,6) < r,1))/(Nx*(Nx-1)/2)    
    else:
        Bm = np.sum(np.triu(np.real(AngDis) < r,1))/(Nx*(Nx-1)/2)
        print('Warning: Complex values ignored')
    if Bm == 1 or Bm == 0:
        CoSi = np.NaN
    else:
        CoSi = -(Bm*np.log(Bm)/np.log(Logx)) - ((1-Bm)*np.log(1-Bm)/np.log(Logx))

    return CoSi, Bm

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