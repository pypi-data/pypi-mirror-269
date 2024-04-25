""" Base Multivariate Permutation Entropy function."""
import numpy as np       
# from itertools import permutations as prm 
from scipy.signal import hilbert

def MvPermEn(Data, m=None, tau=None, Typex=None, tpx=-1, Norm=False, Logx=2):
    """MvPermEn  estimates the multivariate permutation entropy of a multivariate dataset.

    .. code-block:: python
    
        MPerm, MPnorm = MvPermEn(Data) 
    
    Returns the multivariate permutation entropy estimate (``MPerm``) and
    the normalized permutation entropy for the M multivariate sequences in
    ``Data`` using the default parameters:
    embedding dimension = 2*np.ones(M,1), time delay = np.ones(M,1), 
    logarithm = 2, normalisation = w.r.t #symbols (sum(``m-1``))
    
    .. attention::

        The multivariate permutation entropy algorithm implemented here uses
        multivariate embedding based on Takens' embedding theorem, and follows
        the methods for multivariate entropy estimation through shared spatial 
        reconstruction as originally presented by Ahmed & Mandic [1]. 
           
        This function does **NOT** use the multivariate permutation entropy 
        algorithm of Morabito et al. (Entropy, 2012) where the entropy values of 
        individual univariate sequences are averaged because such methods do not
        follow the definition of multivariate embedding and therefore do not
        consider cross-channel statistical complexity.
        
    .. note::
           
        To maximize the number of points in the embedding process, this
        algorithm uses N-max(tau*m) delay vectors and **not** N-max(m)*max(tau)
        as employed in [1].

 
    .. code-block:: python
    
        MPerm, MPnorm = MvPermEn(Data, keyword = value, ...)
        
    Returns the multivariate permutation entropy estimate (``MPerm``) for
    the M multivariate data sequences in ``Data`` using the specified keyword arguments:
        :Data:  - Multivariate dataset, NxM matrix of N (>10) observations (rows) and M (cols) univariate data sequences 
        :m:     - Embedding Dimension, a vector of M positive integers
        :tau:   - Time Delay, a vector of M positive integers
        :Typex: - Permutation entropy variation, can be one of the following strings:
               {``'modified'``, ``'ampaware'``, ``'weighted'``, ``'edge'``, ``'phase'``}
                See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info on MvPermEn variants.    
        :tpx:   - Tuning parameter for associated permutation entropy variation.
             :ampaware:  ``tpx`` is the A parameter, a value in range [0 1] (default = 0.5)
             :edge:      ``tpx`` is the r sensitivity parameter, a scalar > 0 (default = 1)
             :phase:     ``tpx`` is the option to unwrap the phase angle of Hilbert-transformed signal, either [] or 1 (default = 0)
        :Norm:  - Normalisation of MPnorm value, a boolean operator:
             :false:  normalises w.r.t log(# of permutation symbols [sum(m)-1]) - default
             :true:   normalises w.r.t log(# of all possible permutations [sum(m)!])
        :Logx:  - Logarithm base, a positive scalar (defualt = 2; enter 0 for  natural logarithm)

    
    :See also:
        ``PermEn``, ``PermEn2D``, ``XPermEn``, ``MSEn``, ``MvFuzzEn``, ``MvSampEn``.
    
    :References:
      [1] Ahmed Mosabber Uddin, Danilo P. Mandic
            "Multivariate multiscale entropy: A tool for complexity
            analysis of multichannel data."
            Physical Review E 84.6 (2011): 061918.
    
      [2] Christoph Bandt and Bernd Pompe, 
            "Permutation entropy: A natural complexity measure for time series." 
            Physical Review Letters,
            88.17 (2002): 174102.
    
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
    
      [7] Maik Riedl, Andreas Müller, and Niels Wessel,
            "Practical considerations of permutation entropy." 
            The European Physical Journal Special Topics 
            222.2 (2013): 249-262.
    
      [8] Kang Huan, Xiaofeng Zhang, and Guangbin Zhang,
           "Phase permutation entropy: A complexity measure for nonlinear time
           series incorporating phase information."
           Physica A: Statistical Mechanics and its Applications
           568 (2021): 125686.
      """
   
    Data = np.squeeze(Data)
    assert Data.shape[0]>10 and Data.ndim==2 and Data.shape[1]>1,  "Data:   must be an NxM numpy matrix where N>10 and M>1"
    N, Dn = Data.shape 
    if m is None:    m = 2*np.ones(Dn, dtype=int)
    if tau is None:  tau = np.ones(Dn, dtype=int)
    m = m.astype(int)
    tau = tau.astype(int) 
  
    assert isinstance(m,np.ndarray) and all(m>0) and m.size==Dn and m.ndim==1, "m:     must be numpy vector of M positive integers"
    assert isinstance(tau,np.ndarray) and all(tau>0) and tau.size==Dn and tau.ndim==1, "tau:   must be numpy vector of M positive integers"
    assert (isinstance(Typex,str) and Typex.lower() in ['modified','ampaware','weighted','edge','phase']) \
           or Typex is None, "Typex:    must be one of the following strings - 'modified','ampaware','weighted','edge', 'phase'"
    assert isinstance(tpx,(int,float)), \
          "tpx:   the value of tpx relates to 'Typex'. Type help(EntropyHub.MvPermEn) for further info on the 'tpx' value."   
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - False or True"
  
    if Typex is None: Typex = ''
    if Typex.lower() == 'phase':
        Data = np.angle(hilbert(Data,axis=0))
        if tpx == 1:
            Data = np.unwrap(Data)      
    if Logx == 0: Logx = np.exp(1)
    
    Nx = N - max((m-1)*tau)
    Sx = np.zeros((Nx,sum(m)))               
    q = 0 
    for k in range(Dn):
        for p in range(m[k]):
            Sx[:,q] = Data[p*tau[k]:Nx+p*tau[k],  k]
            q += 1
        
    Temp = np.argsort(Sx,axis=1)
    # WAY TOO SLOW - Px = np.asarray(list(prm(np.arange(sum(m)))))
    Px = np.unique(Temp,axis=0)
    Counter = np.zeros(Px.shape[0])
                    
    if Typex.lower() == 'modified':
        Tx = np.diff(np.sort(Sx,axis=1),axis=1)==0    
        for km in range(sum(m)-1):
            Temp[Tx[:,km],km+1] = Temp[Tx[:,km],km]                    

        if Tx.any()>0:   Px = np.vstack((Px,np.unique(Temp[np.any(Tx,axis=1),:],axis=0)))
            
        Counter = np.zeros(Px.shape[0])
        for n in range(Px.shape[0]):
            Counter[n] = np.sum(np.any(Temp - Px[n,:],axis=1)==False)                        
        Counter = Counter[Counter!= 0]
        Ppi = Counter/np.sum(Counter)
        del Tx

    elif Typex.lower() == 'weighted':
        Wj = np.var(Sx,axis=1)                
        for n in range(Px.shape[0]):
            Counter[n] = np.sum(Wj[np.any(Temp - Px[n,:],axis=1)==False])            
        Counter = Counter[Counter!= 0]
        Ppi = Counter/np.sum(Wj)
        del Wj, n

    elif Typex.lower() == 'ampaware':
        if tpx ==-1:
            tpx = 0.5
        elif tpx < 0 or tpx > 1:
            raise Exception('The A parameter (tpx) must be in the range [0 1]')
                              
        AA = np.sum(abs(Sx),axis=1)    
        AB = np.sum(abs(np.diff(Sx,axis=1)),axis=1)               
        Ax = ((tpx*AA/sum(m)) + (1-tpx)*AB/(sum(m)-1))                
        for n in range(Px.shape[0]):
            Counter[n] = np.sum(Ax[np.any(Temp - Px[n,:],axis=1)==False]) # Does Px need 2nd dim?
        Counter = Counter[Counter!= 0]
        Ppi = Counter/np.sum(Ax)                
        del AA, AB, Ax
  
    elif Typex.lower() == 'edge':
        if tpx == -1:
            tpx = 1
        elif tpx <= 0:
            raise Exception('r sensitivity parameter (tpx) must be > 0')
        
        for n in range(Px.shape[0]):
            Tx = np.diff(Sx[np.any(Temp - Px[n],axis=1)==False,:],axis=1)
            Counter[n] = np.sum(np.mean(np.hypot(Tx,1),axis=1)**tpx)
        Counter = Counter[Counter!= 0]
        Ppi = Counter/np.sum(Counter)               
        
    else:
        for n in range(Px.shape[0]):
            Counter[n] = sum(np.any(Temp - Px[n,:],axis=1)==False)            
        Counter = Counter[Counter!=0]
        Ppi = Counter/sum(Counter)
    
    if np.round(np.sum(Ppi),5) != 1:
        print('Warning: Potential error with probability calculation')
           
    with np.errstate(divide='ignore', invalid='ignore'):
        MPerm = -np.sum(Ppi*(np.log(Ppi)/np.log(Logx)))
    
    if Norm:
        MPnorm = MPerm/(np.log(np.math.factorial(sum(m)))/np.log(Logx))
    else:   MPnorm = MPerm/(sum(m)-1)
    
    return MPerm, MPnorm


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