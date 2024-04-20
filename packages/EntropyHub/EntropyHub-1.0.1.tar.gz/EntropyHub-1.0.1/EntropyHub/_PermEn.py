""" Base Permutation Entropy function."""
import numpy as np
from itertools import permutations as prm 
from scipy.signal import hilbert


def PermEn(Sig, m=2, tau=1, Logx=2, Norm=False, Typex='none', tpx=-1):
    """PermEn  estimates the permutation entropy of a univariate data sequence.

    .. code-block:: python
    
        Perm, Pnorm, cPE = PermEn(Sig) 
        
    Returns the permuation entropy estimates (``Perm``), the normalised
    permutation entropy (``Pnorm``) and the conditional permutation entropy (``cPE``)
    for ``m`` = [1,2] estimated from the data sequence (``Sig``) using the default 
    parameters: embedding dimension = 2, time delay = 1, 
    logarithm = base 2, normalisation = w.r.t #symbols (``m-1``)
    Note: using the standard PermEn estimation, ``Perm`` =0 when ``m`` =1. 
    It is recommeneded that signal length, N > 5m! 
    (see [8] and Amigo et al., Europhys. Lett. 83:60005, 2008)
    
    .. code-block:: python
    
        Perm, Pnorm, cPE = PermEn(Sig, m)
        
    Returns the permutation entropy estimates (``Perm``) estimated from the data
    sequence (``Sig``) using the specified embedding dimensions = [1,..., ``m``] 
    with other default parameters as listed above.
 
    .. code-block:: python
    
        Perm, Pnorm, cPE = PermEn(Sig, keyword = value, ...)
        
    Returns the permutation entropy estimates (``Perm``) for dimensions = [1,..., ``m``]
    estimated from the data sequence (``Sig``) using the specified 'keyword' arguments:        
        :m:     - Embedding Dimension, an integer > 1
        :tau:   - Time Delay, a positive integer
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of ``Pnorm`` value, a boolean:
            * False -  normalises w.r.t log(# of permutation symbols [``m-1]``) - default
            *  True  -  normalises w.r.t log(# of all possible permutations [``m!``])
              * Note: Normalised permutation entropy is undefined for ``m`` = 1.
              ** Note: When ``Typex = 'uniquant'`` and ``Norm = True``, normalisation is calculated w.r.t. ``log(tpx^m)`` **
              
        :Typex: - Permutation entropy variation, one of the following: 
                {``'uniquant'``, ``'finegrain'``, ``'modified'``, ``'ampaware'``, ``'weighted'``, ``'edge'``, ``'phase'``}
                 See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info on PermEn variants.    
        :tpx:   - Tuning parameter for associated permutation entropy variation.
                     * [uniquant]  'tpx' is the L parameter, an integer > 1 (default = 4).           
                     * [finegrain] 'tpx' is the alpha parameter, a positive scalar (default = 1)
                     * [ampaware]  'tpx' is the A parameter, a value in range [0 1] (default = 0.5)
                     * [edge]      'tpx' is the r sensitivity parameter, a scalar > 0 (default = 1)
              
        See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info on PermEn variants.    
            
  :See also: 
      ``XPermEn``, ``MSEn``, ``XMSEn``, ``SampEn``, ``ApEn``, ``CondEn``
  
  :References:
      [1] Christoph Bandt and Bernd Pompe, 
          "Permutation entropy: A natural complexity measure for time series." 
          Physical Review Letters,
          88.17 (2002): 174102.

      [2] Xiao-Feng Liu, and Wang Yue,
          "Fine-grained permutation entropy as a measure of natural 
           complexity for time series." 
           Chinese Physics B 
           18.7 (2009): 2690.

      [3] Chunhua Bian, et al.,
          "Modified permutation-entropy analysis of heartbeat dynamics."
          Physical Review E
          85.2 (2012) : 021906

      [4] Bilal Fadlallah, et al.,
          "Weighted-permutation entropy: A complexity measure for time 
          series incorporating amplitude information." 
          Physical Review E 
          87.2 (2013): 022911.

      [5] Hamed Azami and Javier Escudero,
          "Amplitude-aware permutation entropy: Illustration in spike 
          detection and signal segmentation." 
          Computer methods and programs in biomedicine,
          128 (2016): 40-51.

      [6] Zhiqiang Huo, et al.,
          "Edge Permutation Entropy: An Improved Entropy Measure for 
          Time-Series Analysis," 
          45th Annual Conference of the IEEE Industrial Electronics Soc,
          (2019), 5998-6003

      [7] Zhe Chen, et al. 
          "Improved permutation entropy for measuring complexity of time
          series under noisy condition." 
          Complexity 
          1403829 (2019).

      [8] Maik Riedl, Andreas Müller, and Niels Wessel,
          "Practical considerations of permutation entropy." 
          The European Physical Journal Special Topics 
          222.2 (2013): 249-262.

      [9] Kang Huan, Xiaofeng Zhang, and Guangbin Zhang,
          "Phase permutation entropy: A complexity measure for nonlinear time 
          series incorporating phase information." 
          Physica A: Statistical Mechanics and its Applications 
          568 (2021): 125686.   

    """

    Sig = np.squeeze(Sig)          
    N = Sig.shape[0]
    if Logx == 0:
        Logx = np.exp(1)
    
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - False or True"
    assert Typex.lower() in ['none','uniquant','finegrain','modified','ampaware','weighted','edge','phase'] \
            and isinstance(Typex,str), "Typex:    must be one of the following strings - \
            'none','uniquant','finegrain','modified','ampaware','weighted','edge', 'phase'"
    assert isinstance(tpx,(int,float)), \
            "tpx:   the value of tpx relates to 'Typex'. \
             Type help(EntropyHub.PermEn) for further info on the 'tpx' value."   
             
    if Typex.lower() == 'phase':
        Sig = np.angle(hilbert(Sig))
        if tpx == 1:
            Sig = np.unwrap(Sig)

    Sx = np.zeros((N,m))               
    Perm = np.zeros(m)
    Pnorm = np.zeros(m)
    for k in range(m):
        Nx = N-(k*tau)
        Sx[:Nx,k] = Sig[(k*tau):N]
        Temp = np.argsort(Sx[:Nx,:k+1],axis=1)
        Px = np.asarray(list(prm(np.arange(k+1))))
        Counter = np.zeros(Px.shape[0])
                
        if Typex.lower() == 'uniquant':
            Temp = np.sort(Sx[:Nx,:k+1],axis=1)
            S = np.zeros(Temp.shape)
            if tpx == -1:
                tpx = 4
            elif tpx <= 1:
                raise Exception('L parameter must be an integer > 1')
            elif not isinstance(tpx,int):
                raise Exception('L parameter must be an integer')
            
            delta = np.ptp(Sig)/tpx;
            S[:,0] = np.digitize(Temp[:,0],np.arange(min(Sig),max(Sig),delta))            
            if k > 0:
                tt = Temp[:,1:k+1] - np.transpose(np.tile(Temp[:,0],(k,1)))
                S[:,1:k+1] = np.transpose(np.tile(S[:,0],(k,1))) + np.floor(tt/delta)
                del tt

            Px = np.unique(S,axis=0)
            Counter = np.zeros(Px.shape[0])
            for n in range(len(Px)):
                Counter[n] = sum(np.any(S - Px[n,:],axis=1)==False)       
            Counter = Counter[Counter!=0]
            Ppi = Counter/sum(Counter)
            Norm = 3            
            del S, delta, n,
            
        elif Typex.lower() == 'finegrain':  
            
            if k>0:
                if tpx == -1:
                    tpx = 1
                elif tpx <= 0:
                    raise Exception('Alpha parameter must be greater than 0')
                
                q =  np.floor(np.max(abs(np.diff(Sx[:Nx,:k+1],axis=1)),axis=1)/(tpx*np.std(abs(np.diff(Sig)))))
                Temp = np.concatenate((Temp,np.expand_dims(q,1)),axis=1)
                Px = np.unique(Temp,axis=0)
                Counter = np.zeros(Px.shape[0])
                for n in range(Px.shape[0]):
                    Counter[n] = sum(np.any(Temp - Px[n,:],axis=1)==False) 
                Counter = Counter[Counter!=0]
                Ppi = Counter/sum(Counter)
                del q, n
            else:
                Ppi = 1
            
        elif Typex.lower() == 'modified':
            if k > 0:                
                Tx = np.diff(np.sort(Sx[:Nx,:k+1],axis=1),axis=1)==0    
                for km in range(k):
                    Temp[Tx[:,km],km+1] = Temp[Tx[:,km],km]                    
                #Px = np.unique(Temp,axis=0) #This is much slower than unique on it's own
                if Tx.any()>0:
                    Px = np.vstack((Px,np.unique(Temp[np.any(Tx,axis=1),:],axis=0)))
                Counter = np.zeros(Px.shape[0])
                for n in range(Px.shape[0]):
                    Counter[n] = np.sum(np.any(Temp - Px[n,:],axis=1)==False)                        
                Counter = Counter[Counter!= 0]
                Ppi = Counter/np.sum(Counter)
                del Tx
            else:
                Ppi = 1
        
        elif Typex.lower() == 'weighted':
            if k > 0:
                Wj = np.var(Sx[:Nx,:k+1],axis=1)                
                for n in range(Px.shape[0]):
                    Counter[n] = np.sum(Wj[np.any(Temp - Px[n,:],axis=1)==False])            
                Counter = Counter[Counter!= 0]
                Ppi = Counter/np.sum(Wj)
                del Wj, n
            else:
                Ppi = 1
            
        elif Typex.lower() == 'ampaware':
            if k > 0:
                if tpx ==-1:
                    tpx = 0.5
                elif tpx < 0 or tpx > 1:
                    raise Exception('The A parameter (tpx) must be in the range [0 1]')
                                      
                AA = np.sum(abs(Sx[:Nx,:k+1]),axis=1)    
                AB = np.sum(abs(np.diff(Sx[:Nx,:k+1],axis=1)),axis=1)               
                Ax = ((tpx*AA/(k+1)) + (1-tpx)*AB/(k))                
                for n in range(Px.shape[0]):
                    Counter[n] = np.sum(Ax[np.any(Temp - Px[n,:],axis=1)==False]) # Does Px need 2nd dim?
                Counter = Counter[Counter!= 0]
                Ppi = Counter/np.sum(Ax)                
                del AA, AB, Ax
            else:
                Ppi = 1 
        
        elif Typex.lower() == 'edge':
            if tpx == -1:
                tpx = 1
            elif tpx <= 0:
                raise Exception('r sensitivity parameter (tpx) must be > 0')
            
            if k > 0:
                for n in range(Px.shape[0]):
                    Sy = Sx[:Nx,:k+1]
                    Tx = np.diff(Sy[np.any(Temp - Px[n],axis=1)==False,:k+1],axis=1)
                    Counter[n] = np.sum(np.mean(np.hypot(Tx,1),axis=1)**tpx)
                Counter = Counter[Counter!= 0]
                Ppi = Counter/np.sum(Counter)
            else:
                Ppi = 1              
            
        else:
            for n in range(Px.shape[0]):
                Counter[n] = sum(np.any(Temp - Px[n,:],axis=1)==False)            
            Counter = Counter[Counter!=0]
            Ppi = Counter/sum(Counter)
        
        if np.round(np.sum(Ppi),3) != 1:
            print('Warning: Potential error with probability calculation')
               
        Perm[k] = -np.sum(Ppi*(np.log(Ppi)/np.log(Logx)))
        
        if Norm == 3:
            Pnorm[k] = Perm[k]/(np.log(tpx**(k+1))/np.log(Logx))
        
        elif Norm and k>0:
            Pnorm[k] = Perm[k]/(np.log(np.math.factorial(k+1))/np.log(Logx))
                
        elif not Norm and k>0:
            Pnorm[k] = Perm[k]/k  
            
        else:
            Pnorm[k] = np.nan
        
        del Temp, Ppi, Counter

    cPE = np.diff(Perm)
    return Perm, Pnorm, cPE
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