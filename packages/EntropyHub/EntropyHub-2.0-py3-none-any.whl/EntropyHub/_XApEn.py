"""Base Cross Approximate Entropy function."""
import numpy as np    

def XApEn(*Sig, m=2, tau=1, r=None, Logx=np.exp(1)):
    """XApEn  estimates the cross-approximate entropy between two univariate data sequences.

    .. code-block:: python
    
        XAp, Phi = XApEn(Sig1, Sig2)
        
    Returns the cross-approximate entropy estimates (``XAp``) and the average
    number of matched vectors (``Phi``) for ``m`` = [0,1,2], estimated for the data
    sequences contained in ``Sig1`` and ``Sig2`` using the default parameters:
    embedding dimension = 2, time delay = 1, 
    radius threshold = 0.2*SDpooled(``Sig1``,``Sig2``),  logarithm = natural
    
    **NOTE: ``XApEn`` is direction-dependent. Thus, ``Sig1`` is used as the template data sequence, and ``Sig2`` is the matching sequence.
 
     .. code-block:: python
       
         XAp, Phi = XApEn(Sig1, Sig2, keyword = value, ...)
        
    Returns the cross-approximate entropy estimates (``XAp``) between the data
    sequences contained in ``Sig1`` and ``Sig2`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension,  a positive integer   [default: 2]
        :tau:   - Time Delay, a positive integer        [default: 1]
        :r:     - Radius Distance Threshold, a positive scalar [default: 0.2*SDpooled(``Sig1``,``Sig2``)]
        :Logx:  - Logarithm base, a positive scalar     [default: natural]
 
    :See also:
        ``XSampEn``, ``XFuzzEn``, ``XMSEn``, ``ApEn``, ``SampEn``, ``MSEn``
    
    :References:
        [1] Steven Pincus and Burton H. Singer,
            "Randomness and degrees of irregularity." 
            Proceedings of the National Academy of Sciences 
            93.5 (1996): 2083-2088.
    
        [2] Steven Pincus,
            "Assessing serial irregularity and its implications for health."
            Annals of the New York Academy of Sciences 
            954.1 (2001): 245-267.
    
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
    assert isinstance(r,(int,float)) and (r>=0), "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    
    Counter = 1*(abs(np.expand_dims(S1,axis=1) - np.expand_dims(S2,axis=0))<= r)
    M = np.hstack((m*np.ones(N-m*tau), np.repeat(np.arange(m-1,0,-1),tau)))
    XAp = np.zeros((m+1))
    Phi = np.zeros((m+2))    
    for n in range(M.shape[0]):
        ix = np.where(Counter[n, :] == 1)[0]        
        for k in range(1, int(M[n]+1)):
            ix = ix[ix + (k*tau) < N2]     
            if not len(ix):   break            
            p1 = np.tile(S1[n:n+1+(tau*k):tau], (ix.shape[0], 1))                       
            p2 = S2[np.expand_dims(ix,axis=1) + np.arange(0,(k*tau)+1,tau)]           
            ix = ix[np.amax(abs(p1-p2), axis=1) <= r] 
            Counter[n, ix] += 1
            
    #Phi[0] = (np.log(N)/np.log(Logx))/N
    # Phi[1] = np.mean(np.log(np.sum(Counter>0,axis=0)/N)/np.log(Logx))
    Temp = np.sum(Counter>0,axis=0); Temp = Temp[Temp!=0]
    Phi[1] = np.mean(np.log(Temp/N)/np.log(Logx))
    XAp[0]  = Phi[0] - Phi[1]
    
    for k in range(m):
        ai = np.sum(Counter>k+1,axis=0)/(N-(k+1)*tau)
        bi = np.sum(Counter>k,axis=0)/(N-(k*tau))
        ai = ai[ai>0]
        bi = bi[bi>0]
        
        with np.errstate(divide='ignore', invalid='ignore'):
            Phi[k+2] = np.sum(np.log(ai)/np.log(Logx))/(N-(k+1)*tau)
            XAp[k+1]  = np.sum(np.log(bi)/np.log(Logx))/(N-(k*tau)) - Phi[k+2]
        
    return XAp, Phi

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