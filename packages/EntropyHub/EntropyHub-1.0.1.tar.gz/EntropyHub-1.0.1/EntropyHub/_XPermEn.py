"""Base Cross Permutation Entropy function."""
import numpy as np

def XPermEn(*Sig, m=3, tau=1, Logx=np.exp(1)):
    """XPermEn  estimates the cross-permutation entropy between two univariate data sequences.

    .. code-block:: python
    
        XPerm = XPermEn(Sig1, Sig2) 
        
    Returns the cross-permuation entropy estimates (``XPerm``) estimated betweeen
    the data sequences contained in ``Sig1`` and ``Sig2`` using the default parameters:
    embedding dimension = 3, time delay = 1, logarithm = base 2, 
    
    .. code-block:: python
 
        XPerm = XPermEn(Sig1, Sig2, keyword = value, ...)
        
    Returns the permutation entropy estimates (``Perm``) estimated between the data
    sequences contained in ``Sig1`` and ``Sig2`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 2   [default: 3]
            **Note: ``XPerm`` is undefined for embedding dimensions < 3.
        :tau:   - Time Delay, a positive integer        [default: 1]
        :Logx:  - Logarithm base, a positive scalar     [default: 2]   (enter 0 for natural log). 
 
    :See also:
        ``PermEn``, ``XApEn``, ``XSampEn``, ``XFuzzEn``, ``XMSEn``
  
    :References:
        [1] Wenbin Shi, Pengjian Shang, and Aijing Lin,
            "The coupling analysis of stock market indices based on 
            cross-permutation entropy."
            Nonlinear Dynamics
            79.4 (2015): 2439-2447.
     
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
        assert len(S1)==len(S2),  "Sig1/Sig2:   Each sequence must be of equal length"
        
    N1 = S1.shape[0]
    N2 = S2.shape[0]
    
    assert N1>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"
    assert isinstance(m,int) and (m > 2), "m:     must be an integer > 2"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
        
    N = N1-(m-1)*tau
    Sx1 = np.zeros((N,m))
    Sx2 = np.zeros((N,m))    
    for k in range(m):
        Sx1[:,k] = S1[k*tau:N+k*tau]
        Sx2[:,k] = S2[k*tau:N+k*tau]        
    
    Temp = np.argsort(Sx1,axis=1)
    Gx = np.zeros((N,m))
    for k in range(N):
        Gx[k,:] = Sx2[k,Temp[k,:]]
        
    Kt = np.zeros((m-2,m-2,N))
    for k in range(m-2):
        for j in range(k+1,m-1):
            G1 = Gx[:,j+1] - Gx[:,k]
            G2 = Gx[:,k] - Gx[:,j]
            Kt[k,j-1,:] = (G1*G2 > 0)
     
    Di = np.squeeze(np.sum(np.sum(Kt,1),0))
    Ppi,_ = np.histogram(Di,np.arange(-.5,((m-2)*(m-1)+2)/2))
    Ppi = Ppi[Ppi!=0]/N
    XPerm = -sum(Ppi*(np.log(Ppi)/np.log(Logx)))
    
    if round(sum(Ppi),6)!=1:
        print('Warning: Potential error with probability calculation')
        
    return XPerm
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