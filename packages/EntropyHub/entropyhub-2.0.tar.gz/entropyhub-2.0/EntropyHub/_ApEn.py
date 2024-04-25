import numpy as np           
""" Base Approximate Entropy function."""

def ApEn(Sig, m=2, tau=1, r=None, Logx=np.exp(1)):
    """ApEn  estimates the approximate entropy of a univariate data sequence.
        
    .. code-block:: python
        
        Ap, Phi = ApEn(Sig)
    
    Returns the approximate entropy estimates (``Ap``) and the log-average number of 
    matched vectors (``Phi``) for ``m`` = [0,1,2], estimated for the data sequence (``Sig``)
    using the default parameters:
    embedding dimension = 2, time delay = 1, radius threshold = 0.2*SD(``Sig``), logarithm = natural
    
    .. code-block:: python
        
        Ap, Phi = ApEn(Sig, keyword = value, ...)
    
    Returns the approximate entropy estimates (``Ap``) of the data sequence (``Sig``)
    for dimensions = [0, 1, ..., ``m``] using the specified keyword arguments:
          :m:  - Embedding Dimension, a positive integer
          :tau: - Time Delay, a positive integer
          :r:  - Radius Distance Threshold, a positive scalar  
          :Logx: - Logarithm base, a positive scalar 
    
    :See also:
        ``XApEn``, ``SampEn``, ``MSEn``, ``FuzzEn``, ``PermEn``, ``CondEn``, ``DispEn``
    
    :References:
        [1] Steven M. Pincus, 
            "Approximate entropy as a measure of system complexity." 
            Proceedings of the National Academy of Sciences 
            88.6 (1991): 2297-2301.
    
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]
    if r is None:
        r = 0.2*np.std(Sig)
        
    assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and (r>=0), "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"

    Counter = 1*(abs(np.expand_dims(Sig,axis=0) -np.expand_dims(Sig,axis=1))<= r)  
    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))
    Ap = np.zeros((m+1))
    Phi = np.zeros((m+2))    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]
        
        for k in range(1, int(M[n]+1)):
            ix = ix[ix + (k*tau) < N]     
            p1 = np.tile(Sig[n: n + 1 + (tau*k):tau], (ix.shape[0], 1))                       
            p2 = Sig[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]           
            ix = ix[np.amax(abs(p1 - p2), axis=1) <= r] 
            Counter[n, ix] += 1
            
    #Phi[0] = (np.log(N)/np.log(Logx))/N
    Phi[1] = np.mean(np.log(np.sum(Counter>0,axis=0)/N)/np.log(Logx))
    Ap[0]  = Phi[0] - Phi[1]
    
    for k in range(m):
        ai = np.sum(Counter>k+1,axis=0)/(N-(k+1)*tau)
        bi = np.sum(Counter>k,axis=0)/(N-(k*tau))
        ai = ai[ai>0]
        bi = bi[bi>0]
        
        with np.errstate(divide='ignore', invalid='ignore'):
            Phi[k+2] = np.sum(np.log(ai)/np.log(Logx))/(N-(k+1)*tau)
            Ap[k+1]  = np.sum(np.log(bi)/np.log(Logx))/(N-(k*tau)) - Phi[k+2]
        
    return Ap, Phi

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