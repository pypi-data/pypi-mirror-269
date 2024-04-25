""" Base Multivariate Dispersion Entropy function."""
import numpy as np 
from scipy.special import ndtr
from scipy.cluster.vq import kmeans2 
from itertools import combinations as cmb # permutations as prm,
     

def MvDispEn(Data, m=None, tau=None, c=3, Typex='NCDF', Methodx='v1', Norm=False, Logx=np.exp(1)):
    """MvDispEn  estimates the multivariate dispersion entropy of a multivariate dataset.

    .. code-block:: python
    
        MDisp, RDE = MvDispEn(Data)
    
    Returns the multivariate dispersion entropy estimate (``MDisp``) and
    the reverse dispersion entropy (``RDE``) for the M multivariate sequences 
    in ``Data`` using the default parameters:
    embedding dimension = 2*np.ones(M,1), time delay = np.ones(M,1), # symbols = 3, 
    algorithm method = 'v1' (see below), data transform = normalised cumulative density function (ncdf)
    logarithm = natural, data normalization = true,
    
    
    .. important::

        By default, ``MvDispEn`` uses the method termed ``mvDEii`` in [1],
        which follows the original multivariate embedding approach of Ahmed & Mandic [2].
        The ``v1`` method therefore returns a singular entropy estimate.
           
        If the ``v2`` method is selected (``Methodx=='v2'``), the main method
        outlined in [1] termed ``mvDE`` is applied. In this case, entropy is estimated
        using each combination of multivariate delay vectors with lengths 1:max(m),
        with each entropy value returned accordingly. See [1] for more info.

 
    .. code-block:: python
    
        MDisp, RDE = MvDispEn(Data, keyword = value, ...)
        
    Returns the multivariate dispersion entropy estimate (``MDisp``) for the M
    multivariate data sequences in ``Data`` using the specified keyword arguments:
        :Data:     - Multivariate dataset, NxM matrix of N (>10) observations (rows) and M (cols) univariate data sequences
        :m:        - Embedding Dimension, a vector of M positive integers
        :tau:      - Time Delay, a vector of M positive integers
        :c:        - Number of symbols in transform, an integer > 1
        :Methodx:  - The method of multivariate dispersion entropy estimation as outlined in [1], either:
                :``'v1'``:                     employs the method consistent with the original multivariate 
                    embedding approach of Ahmed &  Mandic [2], termed ``mvDEii`` in [1]. (default)
                :``'v2'``:                      employs the main method derived in [1],  termed ``mvDE``.
        :Typex:    - Type of data-to-symbolic sequence transform, one of the following strings   {``'linear'``, ``'kmeans'``, ``'ncdf'``, ``'equal'``}
                     See the `EntropyHub Guide` for more info on these transforms.
        :Logx:  - Logarithm base, a positive scalar
        :Norm:  - Normalisation of ``MDisp`` and ``RDE`` values, a boolean:
                 :false:      no normalisation (default)
                 :true:       normalises w.r.t number of possible dispersion patterns (``c^m``).

    :See also:
        ``DispEn``, ``DispEn2D``, ``MvSampEn``, ``MvFuzzEn``, ``MvPermEn``, ``MSEn``
    
    :References:
      [1] H Azami, A Fernández, J Escudero
          "Multivariate Multiscale Dispersion Entropy of Biomedical Times Series"
          Entropy 2019, 21, 913.

      [2] Ahmed Mosabber Uddin, Danilo P. Mandic
          "Multivariate multiscale entropy: A tool for complexity
          analysis of multichannel data."
          Physical Review E 84.6 (2011): 061918.

      [3] Mostafa Rostaghi and Hamed Azami,
           "Dispersion entropy: A measure for time-series analysis." 
           IEEE Signal Processing Letters 
           23.5 (2016): 610-614.

      [4] Hamed Azami and Javier Escudero,
           "Amplitude-and fluctuation-based dispersion entropy." 
           Entropy 
           20.3 (2018): 210.

      [5] Li Yuxing, Xiang Gao and Long Wang,
           "Reverse dispersion entropy: A new complexity measure for sensor signal." 
           Sensors 
           19.23 (2019): 5203.
        
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
    assert isinstance(c,int) and (c > 1), "c:     must be an integer > 1"
    assert Typex.lower() in ['linear','kmeans','ncdf','equal'], \
                "Typex:    must be one of the following strings - 'linear', 'kmeans', 'ncdf', 'equal'"     
    assert isinstance(Methodx,str) and Methodx.lower() in ['v1','v2'], "Methodx:   must be either 'v1' or 'v2'"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - False or True"
       
    if Logx == 0: Logx = np.exp(1)
    
    Sx = np.zeros((N,Dn), dtype=np.int8)               
    for q in range(Dn):
        Sig = Data[:,q]        
        
        if Typex.lower() == 'linear':
            Zi = np.digitize(Sig,np.arange(min(Sig),max(Sig),np.ptp(Sig)/c))
            
        elif Typex.lower() == 'kmeans':        
            Clux, Zx = kmeans2(Sig, c, iter=200)
            Zx += 1;  xx = np.argsort(Clux) + 1;     Zi = np.zeros(N);
            for k in range(1,c+1):
                Zi[Zx==xx[k-1]] = k;
                
            del Zx, Clux, xx
            
        elif Typex.lower() == 'ncdf':  
            Zx = ndtr((Sig-np.mean(Sig))/np.std(Sig))
            Zi = np.digitize(Zx,np.arange(0,1,1/c))              
            del Zx
                             
        elif Typex.lower() == 'equal':
            ix = np.argsort(Sig, kind='mergesort')
            xx = np.round(np.arange(0,2*N,N/c)).astype(int)
            Zi = np.zeros(N)
            for k in range(c):
                Zi[ix[xx[k]:xx[k+1]]] = k+1 
            del ix, xx, k  
    
        Sx[:,q] = Zi
    
    Nx = N - max((m-1)*tau)
    Vex = np.zeros((Nx,sum(m)), dtype=np.int8)               
    q = 0 
    for k in range(Dn):
        for p in range(m[k]):
            Vex[:,q] = Sx[p*tau[k]:Nx+p*tau[k],  k]
            q += 1
        
                   
    if Methodx.lower() == 'v1':
        Px = np.unique(Vex,axis=0)
        Counter = np.zeros(Px.shape[0])
        for n in range(Px.shape[0]):
            Counter[n] = sum(np.any(Vex - Px[n,:],axis=1)==False)            
        Counter = Counter[Counter!=0]
        Ppi = Counter/sum(Counter)
        
        assert np.round(np.sum(Ppi),5) == 1, 'Warning: Potential error with probability calculation'
           
        with np.errstate(divide='ignore', invalid='ignore'):
            MDisp = -np.sum(Ppi*(np.log(Ppi)/np.log(Logx)))
            RDE = sum((Ppi - (1/(c**float(np.sum(m)))))**2)
            
        if Norm:
            MDisp = MDisp/(np.log(c**float(sum(m)))/np.log(Logx))
            RDE = RDE/(1-(1/(c**float(sum(m)))))

    
    elif Methodx.lower() == 'v2':
        P = sum(m)
        MDisp = np.zeros(max(m))
        RDE = np.zeros(max(m))
        for k in range(1,max(m)+1):
            print(' .', end='')
            Temp = np.array(list(cmb(np.arange(P),k)))
            Vez = np.zeros((Nx*nchk(P,k),k),dtype=np.int8)
            for q in range(Temp.shape[0]):
                Vez[q*Nx:(q+1)*Nx,:] = Vex[:,Temp[q]] 
            
            Px = np.unique(Vez,axis=0)
            Counter = np.zeros(Px.shape[0])
            for n in range(Px.shape[0]):
                Counter[n] = np.sum(np.any(Vez - Px[n,:],axis=1)==False)            
            Counter = Counter[Counter!=0]
            Ppi = Counter/np.sum(Counter)
        
            assert np.round(np.sum(Ppi),5) == 1, 'Warning: Potential error with probability calculation'
           
            with np.errstate(divide='ignore', invalid='ignore'):
                MDisp[k-1] = -np.sum(Ppi*(np.log(Ppi)/np.log(Logx)))
                RDE[k-1] = np.sum((Ppi - (1/(c**float(k))))**2)
        
            if Norm:
                MDisp[k-1] = MDisp[k-1]/(np.log(c**float(k))/np.log(Logx))
                RDE[k-1] = RDE[k-1]/(1-(1/(c**float(k))))
    
    return MDisp, RDE


def nchk(a,b):
    return int(np.math.factorial(a)/(np.math.factorial(b)*np.math.factorial(a-b)))

    
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