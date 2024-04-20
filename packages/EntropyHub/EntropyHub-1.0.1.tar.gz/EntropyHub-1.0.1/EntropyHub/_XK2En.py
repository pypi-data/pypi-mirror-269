"""Base cross-Kolmogorov Entropy function."""
import numpy as np

def XK2En(*Sig, m=2, tau=1 , r=None, Logx=np.exp(1)):
    """XK2En  estimates the cross-Kolmogorov entropy between two univariate  data sequences.

    .. code-block:: python
    
        XK2, Ci = XK2En(Sig1, Sig2) 
        
    Returns the cross-Kolmogorov entropy estimates (``XK2``) and the correlation
    integrals (``Ci``) for ``m`` = [1, 2] estimated between the data sequences 
    contained in ``Sig1`` and``Sig2`` using the default parameters: 
    embedding dimension = 2, time delay = 1, 
    distance threshold (``r``) = 0.2*SDpooled(``Sig1``,``Sig2``), logarithm = natural
 
    .. code-block:: python
    
        XK2, Ci = XK2En(Sig1,Sig2, keyword = value, ...)
        
    Returns the cross-Kolmogorov entropy estimates (``XK2``) estimated between
    the data sequences contained in ``Sig1`` and ``Sig2`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer [default: 2]
        :tau:   - Time Delay, a positive integer         [default: 1]
        :r:     - Radius Distance Threshold, a positive scalar [default: 0.2*SDpooled(``Sig1``,``Sig2``),]
        :Logx:  - Logarithm base, a positive scalar      [default: natural]
     
    :See also:
        ``XSampEn``, ``XFuzzEn``, ``XApEn``, ``K2En``, ``XMSEn``, ``XDistEn``
    
    :References:
        [1] Matthew W. Flood,
            "XK2En - EntropyHub Project"
            (2021) https://github.com/MattWillFlood/EntropyHub
    
    """
 
    assert len(Sig)<=2,  """Input arguments to be passed as data sequences:
        - A single Nx2 numpy matrix with each column representing Sig1 and Sig2 respectively.       \n or \n
        - Two individual numpy vectors representing Sig1 and Sig2 respectively."""
    if len(Sig)==1:
        Sig = np.squeeze(Sig)
        assert max(Sig.shape)>10 and min(Sig.shape)==2,  """Input arguments to be passed as data sequences:
            - A single Nx2 numpy matrix with each column representing Sig1 and Sig2 respectively.       \n or \n
            - Two individual numpy vectors representing Sig1 and Sig2 respectively."""
        if Sig.shape[0] == 2:
            Sig = Sig.transpose()  
        S1 = Sig[:,0]; S2 = Sig[:,1]     
        
    elif len(Sig)==2:
        S1 = np.squeeze(Sig[0])
        S2 = np.squeeze(Sig[1])
        
    N  = S1.shape[0]
    N2 = S2.shape[0]
    if r is None:
        r = 0.2*np.sqrt((np.var(S1)*(N-1) + np.var(S2)*(N2-1))/(N+N2-1))
    
    assert N>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"

    m = m+1
    Z1 = np.zeros((N,m))  
    Z2 = np.zeros((N2,m))  
    Ci = np.zeros(m)
    for n in range(m):
        Nx = N - n*tau
        Z1[:Nx,n] = S1[n*tau:]
        Ny = N2 - n*tau
        Z2[:Ny,n] = S2[n*tau:]            
        Norm = np.zeros((Nx,Ny))             
        for k in range(Nx):
            Temp = np.tile(Z1[k,:n+1],(Ny,1)) - Z2[:Ny,:n+1]
            Norm[k,:] = np.linalg.norm(Temp,axis=1)                      
        Ci[n] = np.mean(Norm[:] < r)
               
    # m = m+1
    # Z1 = np.zeros((N,m))  
    # Z2 = np.zeros((N,m))  
    # Ci = np.zeros(m)
    # for n in range(m):
    #     N2 = N - n*tau
    #     Z1[:N2,n] = Sig[n*tau:,0]
    #     Z2[:N2,n] = Sig[n*tau:,1]            
    #     Norm = np.zeros((N2,N2))             
    #     for k in range(N2):
    #         Temp = np.tile(Z1[k,:n+1],(N2,1)) - Z2[:N2,:n+1]
    #         Norm[k,:] = np.linalg.norm(Temp,axis=1)                      
    #     Ci[n] = np.mean(Norm[:] < r)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        XK2 = (np.log(Ci[:-1]/Ci[1:])/np.log(Logx))/tau
    XK2[np.isinf(XK2)] = np.NaN    
    return  XK2, Ci

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