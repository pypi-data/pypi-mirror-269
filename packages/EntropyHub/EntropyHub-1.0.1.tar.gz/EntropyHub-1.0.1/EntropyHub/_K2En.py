"""Base Kolmogorov Entropy function."""
import numpy as np

def K2En(Sig, m=2, tau=1, r=None, Logx=np.exp(1)):
    """K2En  estimates the Kolmogorov (K2) entropy of a univariate data sequence.

    .. code-block:: python
    
        K2, Ci = K2En(Sig) 
    
    Returns the Kolmogorov entropy estimates (``K2``) and the correlation
    integrals (``Ci``) for ``m`` = [1,2] estimated from the data sequence (``Sig``)
    using the default parameters: embedding dimension = 2, time delay = 1, 
    distance threshold (``r``) = 0.2*SD(``Sig``), logarithm = natural
 
    .. code-block:: python
     
        K2, Ci = K2En(Sig, keyword = value, ...)
        
    Returns the Kolmogorov entropy estimates (``K2``) for dimensions = [1, ..., ``m``]
    estimated from the data sequence (``Sig``) using the 'keyword' arguments:
        :m:    - Embedding Dimension, a positive integer
        :tau:   - Time Delay, a positive integer
        :r:     - Radius Distance Threshold, a positive scalar  
        :Logx:  - Logarithm base, a positive scalar  
 
    :See also: 
        ``DistEn``, ``XK2En``, ``MSEn``    
      
    :References:
        [1] Peter Grassberger and Itamar Procaccia,
            "Estimation of the Kolmogorov entropy from a chaotic signal." 
            Physical review A 28.4 (1983): 2591.
    
        [2] Lin Gao, Jue Wang  and Longwei Chen
            "Event-related desynchronization and synchronization 
            quantification in motor-related EEG by Kolmogorov entropy"
            J Neural Eng. 2013 Jun;10(3):03602
    
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]    
    if r is None:
        r = 0.2*np.std(Sig)
    
    assert N>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m>0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau>0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
               
    m = m+1
    Zm = np.zeros((N,m))  
    Ci = np.zeros(m)
    for n in range(m):
        N2 = N - n*tau
        Zm[:N2,n] = Sig[n*tau:]  
        Norm = np.ones((N2-1,N2-1))*np.inf     
        for k in range(N2-1):
            Temp = np.tile(Zm[k,:n+1],(N2-k-1,1)) - Zm[k+1:N2,:n+1]
            Norm[k,k:] = np.linalg.norm(Temp,axis=1)   
        # Norm[Norm==0] = np.inf;
        Ci[n] = 2*np.sum(Norm < r)/(N2*(N2-1))
    
    with np.errstate(divide='ignore', invalid='ignore'):
        K2 = (np.log(Ci[:-1]/Ci[1:])/np.log(Logx))/tau
    K2[np.isinf(K2)] = np.NaN    
    return  K2, Ci

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