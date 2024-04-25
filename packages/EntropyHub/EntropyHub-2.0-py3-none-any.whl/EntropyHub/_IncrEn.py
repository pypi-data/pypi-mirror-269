"""Base Increment Entropy function."""
import numpy as np

def IncrEn(Sig,  m=2, tau=1, R=4, Logx=2, Norm=False):
    """IncrEn  estimates the increment entropy of a univariate data sequence.
    
    .. code-block:: python
    
        Incr = IncrEn(Sig) 
        
    Returns the increment entropy (``Incr``) estimate of the data sequence (``Sig``)
    using the default parameters: embedding dimension = 2, time delay = 1, quantifying resolution = 4, logarithm = base 2,
 
    .. code-block:: python    
    
        Incr = IncrEn(Sig, keyword = value, ...)
    
    Returns the increment entropy (``Incr``) estimate of the data sequence (``Sig``)
    using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
        :tau:   - Time Delay, a positive integer
        :R:     - Quantifying resolution, a positive scalar
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of ``IncrEn`` value, a boolean:
            * [False]  no normalisation - default
            * [True]   normalises w.r.t embedding dimension (m-1). 
 
    :See also:
        ``PermEn``, ``SyDyEn``, ``MSEn``
    
    :References:
        [1] Xiaofeng Liu, et al.,
            "Increment entropy as a measure of complexity for time series."
            Entropy
            18.1 (2016): 22.1.
    
        ***   "Correction on Liu, X.; Jiang, A.; Xu, N.; Xue, J. - Increment 
            Entropy as a Measure of Complexity for Time Series, Entropy 2016, 18, 22." 
            Entropy 
            18.4 (2016): 133.
    
        [2] Xiaofeng Liu, et al.,
            "Appropriate use of the increment entropy for 
            electrophysiological time series." 
            Computers in biology and medicine 
            95 (2018): 13-23.
    
    """
    
    Sig = np.squeeze(Sig)
    if Logx == 0:
        Logx = np.exp(1)
    
    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(R,int) and R > 0, "R:    must be a positive integer"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"  
                
    Vi = np.diff(np.squeeze(Sig))
    N = Vi.shape[0]  - ((m-1)*tau)
    Vk = np.zeros((N,m))               
    for k in range(m):
        Vk[:,k] = Vi[k*tau:N+(k*tau)]        
        
    Sk = np.sign(Vk)
    Temp = np.tile(np.std(Vk,axis=1,ddof=1,keepdims=True),(1,m))
    Qk = np.minimum(R, np.floor(abs(Vk)*R/Temp))
    Qk[np.any(Temp==0,axis=1),:] = 0
    Wk = Sk*Qk
    Px = np.unique(Wk,axis=0)
    Counter = np.zeros(Px.shape[0])
    
    for k in range(Px.shape[0]):
        Counter[k] = np.sum(np.any(Wk - Px[k,:],axis=1)==False)
    Ppi = Counter/N      
        
    if Px.shape[0] > (2*R + 1)**m:
        print('Possible error with probability estimation')
    elif round(sum(Ppi),3) != 1:
        print('Possible error with probability estimation')
        
    Incr = -sum(Ppi*(np.log(Ppi)/np.log(Logx)))
    if Norm:
        Incr = Incr/(m-1)
    
    return Incr
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