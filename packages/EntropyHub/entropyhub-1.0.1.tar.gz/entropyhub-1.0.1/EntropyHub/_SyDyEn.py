"""Base Symbolic Dynamic Entropy function."""
import numpy as np
from scipy.cluster.vq import kmeans2

def  SyDyEn(Sig, m=2, tau=1, c=3, Typex='MEP', Logx=np.exp(1), Norm=True):
    """SyDyEn  estimates the symbolic dynamic entropy of a univariate data sequence.

    .. code-block:: python
    
        SyDy, Zt = SyDyEn(Sig) 
        
    Returns the symbolic dynamic entropy (``SyDy``) and the symbolic sequence
    (``Zt``) of the data sequence (``Sig``) using the default parameters: 
    embedding dimension = 2, time delay = 1, symbols = 3, logarithm = natural,
    symbolic partition type = maximum entropy partitioning (``'MEP'``), 
    normalisation = normalises w.r.t # possible vector permutations (``c^m``) 
  
    .. code-block:: python
    
        SyDy, Zt = SyDyEn(Sig, keyword = value, ...)
        
    Returns the symbolic dynamic entropy (``SyDy``) and the symbolic sequence
    (``Zt``) of the data sequence (``Sig``) using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer
        :tau:   - Time Delay, a positive integer
        :c:     - Number of symbols, an integer > 1
        :Typex: - Type of symbolic sequence partitioning, one of the following:
         {``'linear'``, ``'uniform'``, ``'MEP'`` (default), ``'kmeans'``} 
        :'Logx:  - Logarithm base, a positive scalar  
        :Norm:  - Normalisation of SyDyEn value, a boolean:
            [False]  no normalisation 
            [True]   normalises w.r.t # possible dispersion patterns (``c^m+1``) - default
  
    See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info on these parameters.
    
    :See also:
        ``DispEn``, ``PermEn``, ``CondEn``, ``SampEn``, ``MSEn``
    
    :References:
        [1] Yongbo Li, et al.,
            "A fault diagnosis scheme for planetary gearboxes using 
            modified multi-scale symbolic dynamic entropy and mRMR feature 
            selection." 
            Mechanical Systems and Signal Processing 
            91 (2017): 295-312. 
    
        [2] Jian Wang, et al.,
            "Fault feature extraction for multiple electrical faults of 
            aviation electro-mechanical actuator based on symbolic dynamics
            entropy." 
            IEEE International Conference on Signal Processing, 
            Communications and Computing (ICSPCC), 2015.
    
        [3] Venkatesh Rajagopalan and Asok Ray,
            "Symbolic time series analysis via wavelet-based partitioning."
            Signal processing 
            86.11 (2006): 3309-3320.
    
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]
            
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(c,int) and (c > 1), "c:     must be an integer > 1"
    assert Typex.lower() in ['linear','uniform','mep','kmeans'], \
            "Typex:   must be one of the following strings - \
            'linear', 'uniform', 'MEP', 'kmeans'" 
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"  
    
    Nx = N-((m-1)*tau)
    if Typex.lower() == 'linear':
        Zt = np.digitize(Sig, np.arange(min(Sig),max(Sig),np.ptp(Sig)/c))
        
    elif Typex.lower() == 'uniform':
        Zt = np.zeros(Sig.shape)
        Ix = np.argsort(Sig)
        # z = np.digitize(np.arange(1,N+1),np.arange(1,N+1,round(N/c)))
        z = np.digitize(np.arange(N),np.arange(0,2*N,N/c))
        Zt[Ix] = z
        
    elif Typex.lower()=='kmeans':
        
        Clux, Zi = kmeans2(Sig, c, iter=200)
        Zi += 1;  xx = np.argsort(Clux) + 1;     Zt = np.zeros(N);
        for k in range(1,c+1):
            Zt[Zi==xx[k-1]] = k;        
        
    else:        # MEP method is default
        Tx = np.sort(Sig)
        Temp = np.hstack((0,np.ceil(np.arange(1,c)*N/c)-1))
        Zt = np.digitize(Sig, Tx[Temp.astype(int)])
        
    Zm = np.zeros((Nx,m))
    for n in range(m):
        Zm[:,n] = Zt[n*tau:Nx+(n*tau)]
    
    T = np.unique(Zm,axis=0)
    Counter = np.zeros(T.shape[0])
    Counter2 = np.zeros((T.shape[0],c))
    Bins = np.arange(0.5,c+1.5,1)
    for n in range(T.shape[0]):
        Ordx = (np.any(Zm - T[n,:],axis=1)==0)  
        Counter[n] = sum(Ordx)/Nx
        Temp = Zm[np.hstack((np.zeros(m*tau,dtype=bool), Ordx[:-(m*tau)])),0]
        Counter2[n,:], _ = np.histogram(Temp,Bins)

    Temp = np.sum(Counter2,axis=1)
    Counter2[Temp>0,:] = Counter2[Temp>0,:]/np.tile(Temp[Temp>0],(c,1)).transpose()    
    Counter2[np.isnan(Counter2)] = 0    
    
    with np.errstate(divide='ignore'):
        P1 = -sum(Counter*np.log(Counter)/np.log(Logx))
        P2 = np.log(np.tile(Counter,(c,1)).transpose()*Counter2)/np.log(Logx)
    P2[np.isinf(P2)] = 0 
    SyDy = P1 - sum(Counter*np.sum(P2,axis=1))
    
    if round(sum(Counter),4) != 1 or max(np.sum(Counter2,axis=1)) != 1:
        print('Potential Error calculating probabilities')
    if Norm:
        SyDy = SyDy/(np.log(c**(m+1))/np.log(Logx))
    
    return SyDy, Zt

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