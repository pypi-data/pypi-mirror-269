import numpy as np           
""" Base Range Entropy function."""

def RangEn(Sig, m=2, tau=1, r=0.2, Methodx='SampEn', Logx=np.exp(1)):
    """RangEn  estimates the range entropy of a univariate data sequence.

    .. code-block:: python
    
        Rangx, A, B = RangEn(Sig) 
        
    Returns the range entropy estimate (``Rangx``) and the number of matched state
    vectors (``m: B``, ``m+1: A``) estimated from the data sequence (``Sig``)
    using the sample entropy algorithm and the following default parameters: 
    embedding dimension = 2, time delay = 1, radius threshold = 0.2, logarithm = natural.    
    
    .. code-block:: python
    
        Rangx, A, B = RangEn(Sig, keyword = value, ...)
        
    Returns the range entropy estimates (``Rangx``) for dimensions = ``m``
    estimated for the data sequence (``Sig``) using the specified keyword arguments:
        :m:         - Embedding Dimension, a positive integer
        :tau:       - Time Delay, a positive integer
        :r:         - Radius Distance Threshold, a positive value between 0 and 1
        :Methodx:   - Base entropy method, either 'SampEn' [default] or 'ApEn'
        :Logx:      - Logarithm base, a positive scalar  
 
    :See also:
        ``ApEn``, ``SampEn``, ``FuzzEn``,  ``MSEn``
  
    :References:
        [1] Omidvarnia, Amir, et al.
            "Range entropy: A bridge between signal complexity and self-similarity"
            Entropy 
            20.12 (2018): 962.
            
        [2] Joshua S Richman and J. Randall Moorman. 
            "Physiological time-series analysis using approximate entropy
            and sample entropy." 
            American Journal of Physiology-Heart and Circulatory Physiology 
            2000

    """
  
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]  
    
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and (r>=0) and (r<=1), "r:     must be a value between 0 and 1"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Methodx,str) and (Methodx.lower() in ['apen','sampen']), "Methodx must be either 'ApEn' or 'SampEn'"
            
    if Methodx.lower() == 'sampen':            
        Nx = N - m*tau
        Sx = np.zeros((Nx,m+1))
        for k in range(m+1):        
            Sx[:,k] = Sig[k*tau:Nx + k*tau]
       
        A = np.zeros(Nx,dtype=int)
        B = np.zeros(Nx,dtype=int)
        for k in range(Nx - 1):            
            Dxy = np.abs(np.tile(Sx[k,:-1],(Nx-(k+1),1)) - Sx[k+1:,:-1])             
            Mx = np.max(Dxy,axis=1)
            Mn = np.min(Dxy,axis=1)
            RR = (Mx - Mn)/(Mx + Mn) <= r
            #RR = Mx <= r
            B[k] = RR.sum()
            
            if B[k]>0:
                Dxy2 = np.abs(np.tile(Sx[k,:],(B[k],1)) - Sx[k+1:,:][RR,:])             
                Mx = np.max(Dxy2,axis=1)
                Mn = np.min(Dxy2,axis=1)
                RR2 = (Mx - Mn)/(Mx + Mn) <= r                            
                #RR2 = Mx <= r
                A[k] = RR2.sum()
                    
        with np.errstate(divide='ignore', invalid='ignore'):
            Rangx = -np.log(A.sum()/B.sum())/np.log(Logx) 
       
            return Rangx, A, B
        
    elif Methodx.lower() == 'apen':
        Nx = N - (m-1)*tau
        Sx = np.zeros((Nx,m))
        for k in range(m):        
            Sx[:,k] = Sig[k*tau:Nx + k*tau]                
        Sx = np.hstack((Sx, np.expand_dims(np.hstack((Sig[m*tau::],np.zeros(tau))), axis=1)))        

        B = np.zeros(Nx,dtype=int)
        A = np.zeros(Nx-tau,dtype=int)
        for k in range(Nx):                    
            Dxy = np.abs(np.tile(Sx[k,:-1],(Nx,1)) - Sx[:,:-1])             
            Mx = np.max(Dxy,axis=1)
            Mn = np.min(Dxy,axis=1)
            RR = (Mx - Mn)/(Mx + Mn) <= r             
            # RR = Mx <= r
            B[k] = RR.sum()
                     
            if k < (Nx - tau):
                RR[-tau:] = False
                Dxy2 = np.abs(np.tile(Sx[k,:],(RR.sum(),1)) - Sx[RR,:])             
                Mx2 = np.max(Dxy2,axis=1)
                Mn2 = np.min(Dxy2,axis=1)
                RR2 = (Mx2 - Mn2)/(Mx2 + Mn2) <= r                     
                # RR2 = Mx2 <= r                       
                A[k] = RR2.sum()
                        
        with np.errstate(divide='ignore', invalid='ignore'):
            Ax = (np.log(A/(Nx-tau))/np.log(Logx)).mean()
            Bx = (np.log(B/Nx)/np.log(Logx)).mean()
            
            Ap = Bx - Ax
       
            return Ap, A, B  
    
    else:
        raise Exception("Methodx must be either 'ApEn' or 'SampEn'")

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