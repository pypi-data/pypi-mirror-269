"""Base Diversity Entropy function."""
import numpy as np 

def DivEn(Sig,  m=2, tau=1, r=5, Logx=np.exp(1)):
    """DivEn  estimates the diversity entropy of a univariate data sequence.
    
    .. code-block:: python
        
        Div, CDEn, Bm = DivEn(Sig) 
        
    Returns the diversity entropy (``Div``), the cumulative diversity entropy (``CDEn``),
    and the corresponding probabilities (``Bm``) estimated from the data sequence (``Sig``) 
    using the default parameters:   embedding dimension = 2, time delay = 1, 
    # bins = 5,  logarithm = natural,

    .. code-block:: python
        
        Div, CDEn, Bm = DivEn(Sig, keyword = value, ...)
        
    Returns the diversity entropy (``Div``) estimated from the data
    sequence (``Sig``) using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, an integer > 1
        :tau:   - Time Delay, a positive integer
        :r:     - Histogram bins #: either
                    * an integer [1 < ``r``] representing the number of bins
                    * a list/numpy array of 3 or more increasing values in range [-1 1] representing the bin edges including the rightmost edge.
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 

    :See also:
        ``CoSiEn``, ``PhasEn``, ``SlopEn``, ``GridEn``, ``MSEn``
    
    :References:            
        [1] X. Wang, S. Si and Y. Li, 
            "Multiscale Diversity Entropy: A Novel Dynamical Measure for Fault 
            Diagnosis of Rotating Machinery," 
            IEEE Transactions on Industrial Informatics,
            vol. 17, no. 8, pp. 5419-5429, Aug. 2021
            
        [2] Y. Wang, M. Liu, Y. Guo, F. Shu, C. Chen and W. Chen, 
            "Cumulative Diversity Pattern Entropy (CDEn): A High-Performance, 
            Almost-Parameter-Free Complexity Estimator for Nonstationary Time Series,"
            IEEE Transactions on Industrial Informatics
            vol. 19, no. 9, pp. 9642-9653, Sept. 2023            
    """
    
    Sig = np.squeeze(Sig)
    N = Sig.shape[0]  
    if Logx == 0:
        Logx = np.exp(1)
        
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert (isinstance(r, int) and r>1) or (isinstance(r, (list,np.ndarray)) and  
            len(r)>2 and min(r)>=-1 and np.ndim(r)==1 and max(r)<=1 and min(np.diff(r))>0), \
            "r:    must be an int > 1 or a list/numpy array of 3 or more increasing values in range [-1 1]"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    
    Nx = N - (m-1)*tau
    Zm = np.zeros((Nx,m))
    for n in range(m):
        Zm[:,n] = Sig[n*tau:Nx+(n*tau)]
        
    Num = np.sum(Zm[:-1,:]*Zm[1:,:],axis=1)
    Den = np.sqrt(np.sum(Zm[1:,:]**2,axis=1))*np.sqrt(np.sum(Zm[:-1,:]**2,axis=1))
    Di = Num/Den
    Bm, _ = np.histogram(Di, bins = r, range=(-1,1))
    Bm = Bm[Bm>0]/sum(Bm)
    
    if np.round(np.sum(Bm),6) != 1:
        print("""Warning:
              Potential error is probability estimation!
              Sum(Pi) == """, np.round(np.sum(Bm),6))
    
    if isinstance(r, (list,np.ndarray)):     r = len(r)-1
    
    Pj = 1 - np.cumsum(Bm);     Pj = (Pj/sum(Pj))[:-1]
    CDEn = -np.sum(Pj*np.log(Pj)/np.log(Logx))/(np.log(r)/np.log(Logx))
    
    Div = -np.sum(Bm*np.log(Bm)/np.log(Logx))/(np.log(r)/np.log(Logx))
        
    return Div, CDEn, Bm                
        

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