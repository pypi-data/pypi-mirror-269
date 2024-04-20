"""Base Entropy of Entropy Function"""    
import numpy as np

def EnofEn(Sig, tau=10, S=10, Xrange=None, Logx=np.exp(1)):
    """EnofEn  estimates the entropy of entropy of a univariate data sequence.
    
    .. code-block:: python

        EoE, AvEn, S2 = EnofEn(Sig) 

    Returns the entropy of entropy (``EoE``), the average Shannon entropy 
    across all windows (``AvEn``), and the number of levels (``S2``) estimated 
    from the data sequence (``Sig``) using  the default parameters: 
    window length (samples) = 10, slices = 10, logarithm = natural
    heartbeat interval range (xmin, xmax) = (min(Sig), max(Sig))

    .. code-block:: python
        
        EoE, AvEn, S2 = EnofEn(Sig, keyword = value, ...)
        
    Returns the entropy of entropy (``EoE``) estimated from the data sequence (``Sig``)  
    using the specified 'keyword' arguments:
        :tau:     - Window length, an integer > 1
        :S:       - Number of slices, an integer > 1
        :Xrange:  - The min and max heartbeat interval, a two-element tuple where X[0] < X[1]
        :Logx:    - Logarithm base, a positive scalar  
 
    :See also::
        ``SampEn``, ``MSEn``
    
    :References:
        [1] Chang Francis Hsu, et al.,
            "Entropy of entropy: Measurement of dynamical complexity for biological systems." 
            Entropy 
            19.10 (2017): 550.
    
    """
        
    Sig = np.squeeze(Sig)
    
    if Xrange is None:
        Xrange = (np.min(Sig),np.max(Sig))

    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(tau,int) and (tau > 1) and (tau<len(Sig)), "tau:   must be an integer > 1 and < length(Sig)"
    assert isinstance(S,int) and S>1, "S:  must be an integer > 1"
    assert isinstance(Xrange,tuple) and Xrange[0]<=Xrange[1] and len(Xrange)==2, \
    "Xrange:  must be a two-element numeric tuple where Xrange[0]<Xrange[1]"   
    
    Wn = int(np.floor(Sig.shape[0]/tau))
    Wj = np.reshape(Sig[:Wn*tau],(Wn,tau))
    Edges = np.linspace(Xrange[0],Xrange[1],S+1)   #Edges = np.linspace(min(Sig),max(Sig),S[0]+1)
    Yj = np.zeros(Wn)
    for n in range(Wn):
        Temp,_ = np.histogram(Wj[n,:],Edges)        
        Temp = Temp[Temp!=0]/tau
        Yj[n] = -sum(Temp*(np.log(Temp)/np.log(Logx)))
        
    AvEn = sum(Yj)/Wn
    #Edges = np.linspace(min(Yj),max(Yj),S[1]+1)
    #Pjl,_ = np.histogram(Yj,Edges)
    #Pjl = Pjl/Wn
    #Pjl = Pjl[Pjl!=0]
    
    _, Tempy = np.unique(np.round(Yj,12), return_counts=True)    
    Pjl = Tempy/Wn
    S2 = len(Pjl)
    
    if round(sum(Pjl),5) != 1:
        print('Warning: Possible error estimating probabilities')
    EoE = -sum(Pjl*(np.log(Pjl)/np.log(Logx)))    
        
    return EoE, AvEn, S2
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