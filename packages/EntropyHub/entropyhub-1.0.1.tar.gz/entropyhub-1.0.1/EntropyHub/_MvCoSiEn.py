""" Base Multivariate Cosine Similarity Entropy function."""
import numpy as np     

def MvCoSiEn(Data, m=None, tau=None, r=0.1, Norm=0, Logx=2):
    """MvCoSiEn  estimates the multivariate cosine similarity entropy of a multivariate dataset.

    .. code-block:: python
    
        MCoSi, Bm = MvCoSiEn(Data) 

    Returns the multivariate cosine similarity entropy estimate (``MCoSi``)
    and the corresponding global probabilities (``Bm``) estimated for the 
    M multivariate sequences in ``Data`` using the default parameters: 
    embedding dimension = 2*np.ones(M,1), time delay = np.ones(M,1), 
    angular threshold = 0.1, logarithm = 2, data normalization = none, 
    
    .. note::

        To maximize the number of points in the embedding process, this algorithm 
        uses N-max(m*tau) delay vectors and **not** N-max(m)*max(tau) as employed 
        in [1][2].
        
  
    .. code-block:: python

         MCoSi, Bm = MvCoSiEn(Data, keyword = value, ...)

    Returns the multivariate cosine similarity entropy estimates (``MCoSi``) 
    estimated from the M multivariate data sequences in ``Data`` using the 
    specified keyword arguments:
        :Data:  - Multivariate dataset, NxM matrix of N (>10) observations (rows) and M (cols) univariate data sequences
        :m:     - Embedding Dimension, a vector of M positive integers
        :tau:   - Time Delay, a vector of M positive integers      
        :r:     - Angular threshold, a value in range [0 < ``r`` < 1]
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of ``Data``, one of the following integers:
                :0:   no normalisation - default
                :1:   remove median(``Data``) to get zero-median series
                :2:   remove mean(``Data``) to get zero-mean series
                :3:   normalises each sequence in ``Data`` to unit variance and zero mean
                :4:   normalises each sequence in ``Data`` values to range [-1 1]
                
              
    :See also:
        ``CoSiEn``, ``MvDispEn``, ``MvSampEn``, ``MvFuzzEn``, ``MvPermEn``, ``MSEn``
    
    :References:
         [1] H. Xiao, T. Chanwimalueang and D. P. Mandic, 
              "Multivariate Multiscale Cosine Similarity Entropy" 
              IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),
              pp. 5997-6001, doi: 10.1109/ICASSP43922.2022.9747282.
    
         [2] Xiao, H.; Chanwimalueang, T.; Mandic, D.P., 
              "Multivariate Multiscale Cosine Similarity Entropy and Its 
              Application to Examine Circularity Properties in Division Algebras."
              Entropy 2022, 24, 1287. 
    
         [3] Ahmed Mosabber Uddin, Danilo P. Mandic
              "Multivariate multiscale entropy: A tool for complexity
              analysis of multichannel data."
              Physical Review E 84.6 (2011): 061918.
    
         [4] Theerasak Chanwimalueang and Danilo Mandic,
              "Cosine similarity entropy: Self-correlation-based complexity
              analysis of dynamical systems."
              Entropy 
              19.12 (2017): 652.
                      
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
    assert isinstance(r, (int,float)) and r > 0 and r < 1, "r:    must be a value in range 0 < r < 1"
    assert isinstance(Logx,(int,float)) and (Logx>=0), "Logx:     must be a positive value"
    assert isinstance(Norm,int) and np.isin(Norm, np.arange(5)), "Norm:     must be an integer in range [0 4]"
       
    if Logx == 0: Logx = np.exp(1)
    
    if Norm == 1:
        Xi = Data - np.median(Data,axis=0)
    elif Norm == 2:
        Xi = Data - np.mean(Data,axis=0)
    elif Norm == 3:
        Xi = (Data - np.mean(Data,axis=0))/np.std(Data,axis=0)
    elif Norm == 4:
        Xi = (2*(Data - np.min(Data,axis=0))/np.ptp(Data,axis=0)) - 1
    else:
        Xi = Data*1 
       
    Nx = N - max((m-1)*tau)
    Zm = np.zeros((Nx,sum(m)))               
    q = 0 
    for k in range(Dn):
        for p in range(m[k]):
            Zm[:,q] = Xi[p*tau[k]:Nx+p*tau[k],  k]
            q += 1
        
    Num = np.inner(Zm,Zm)
    Mag = np.sqrt(np.diag(Num))
    Den = np.outer(Mag, Mag)

    AngDis = np.arccos(np.triu(Num/Den,1))/np.pi    
    if np.max(np.imag(AngDis)) < 10**-6:
        Bm = np.sum(np.triu(np.round(AngDis,6) < r,1))/(Nx*(Nx-1)/2)    
    else:
        Bm = np.sum(np.triu(np.real(AngDis) < r,1))/(Nx*(Nx-1)/2)
        print('Warning: Complex values ignored')
    if Bm == 1 or Bm == 0:
        CoSi = np.NaN
    else:
        CoSi = -(Bm*np.log(Bm)/np.log(Logx)) - ((1-Bm)*np.log(1-Bm)/np.log(Logx))

    return CoSi, Bm

    
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