"""Base Cross Sample Entropy function."""
import numpy as np 

def XSampEn(*Sig, m=2, tau=1, r=None, Logx=np.exp(1), Vcp=False):
    """XSampEn  Estimates the cross-sample entropy between two univariate data sequences.
    
    .. code-block:: python
    
        XSamp, A, B = XSampEn(Sig1, Sig2) 
        
    Returns the cross-sample entropy estimates (``XSamp``) and the number of 
    matched vectors (``m: B``, ``m+1: A``) for ``m`` = [0,1,2] estimated for the two 
    univariate data sequences contained in ``Sig1`` and ``Sig2`` using the default parameters:
    embedding dimension = 2, time delay = 1, radius = 0.2*SDpooled(``Sig1``,``Sig2``),
    logarithm = natural
    
    .. code-block:: python
    
        XSamp, A, B, (Vcp, Ka, Kb) = XSampEn(Sig1, Sig2, ..., Vcp = True) 
    
    If ``Vcp == True``, an additional tuple ``(Vcp, Ka, Kb)`` is returned with    
    the cross-sample entropy estimates (``XSamp``) and the number of matched state
    vectors (``m: B``, ``m+1: A``). ``(Vcp, Ka, Kb)``  contains the variance of the conditional
    probabilities (``Vcp``, i.e. CP = A/B),  and the number of **overlapping**
    matching vector pairs of lengths m+1 (``Ka``) and m (``Kb``),
    respectively.  Note ``Vcp`` is undefined for the zeroth embedding dimension (m = 0) 
    and due to computational demand, **will take substantially more time to return function outputs.**
    See Appendix B in [2] for more info.
 
    .. code-block:: python 
 
         XSamp, A, B = XSampEn(Sig1, Sig2, keyword = value, ...)
                  
    Returns the cross-sample entropy estimates (``XSamp``) for dimensions [0,1,..., ``m``]
    estimated between the data sequences ``Sig1`` and ``Sig2`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer  [default: 2]
        :tau:   - Time Delay, a positive integer         [default: 1]
        :r:     - Radius, a positive scalar              [default: 0.2*SDpooled(``Sig1``,``Sig2``)]
        :Logx:  - Logarithm base, a positive scalar      [default: natural]
 
    :See also:
        ``XFuzzEn``, ``XApEn``, ``SampEn``, ``SampEn2D``, ``XMSEn``, ``ApEn``
    
    :References:
        [1] Joshua S Richman and J. Randall Moorman. 
            "Physiological time-series analysis using approximate entropy
            and sample entropy." 
            American Journal of Physiology-Heart and Circulatory Physiology
            (2000)
        
        [2]  Douglas E Lake, Joshua S Richman, M.P. Griffin, J. Randall Moorman
            "Sample entropy analysis of neonatal heart rate variability."
            American Journal of Physiology-Regulatory, Integrative and Comparative Physiology
            283, no. 3 (2002): R789-R797.
    
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
    assert isinstance(r,(int,float)) and r>=0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Vcp,bool), "Vcp:     must be a Boolean"    

    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))   
    Counter = 1*(abs(np.expand_dims(S1,axis=1) - np.expand_dims(S2,axis=0))<= r)
    A = np.zeros(m+1)
    B = np.zeros(m+1)
    A[0] = np.sum(Counter)
    B[0] = N*N2
    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]        
        for k in range(1,int(M[n]+1)):              
            ix = ix[ix + (k*tau) < N2]
            if not len(ix):    break  
            p1 = np.tile(S1[n: n+1+(tau*k):tau], (ix.shape[0], 1))                       
            p2 = S2[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]
            ix = ix[np.amax(abs(p1 - p2), axis=1) <= r] 
            Counter[n, ix] += 1
    
    for k in range(1, m+1):
        A[k] = np.sum(Counter > k)
        B[k] = np.sum(Counter >= k)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        XSamp = -np.log(A/B)/np.log(Logx)
 
    
    if Vcp:
        T1,T2 = np.expand_dims(np.where(Counter>m),axis=1)
        Ka = np.triu(abs(T1-T1.T)<=m*tau,1) + np.triu(abs(T2-T2.T)<=m*tau,1) 

        T1,T2 = np.expand_dims(np.where(Counter[:,:-m*tau]>=m),axis=1)
        Kb = np.triu(abs(T1-T1.T)<=(m-1)*tau,1) + np.triu(abs(T2-T2.T)<=(m-1)*tau,1) 
                    
        Ka = np.sum(Ka)
        Kb = np.sum(Kb)
        CP = A[-1]/B[-1]
        Vcp = (CP*(1-CP)/B[-1]) + (Ka - Kb*(CP**2))/(B[-1]**2)

        return XSamp, A, B, (Vcp, Ka, Kb)
    
    else:
        return XSamp, A, B     


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