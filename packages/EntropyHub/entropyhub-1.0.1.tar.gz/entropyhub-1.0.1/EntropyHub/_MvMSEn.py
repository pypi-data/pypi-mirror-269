"Base Multivariate Multiscale Entropy function."
import numpy as np   
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy
# from scipy.stats import moment

def MvMSEn(Data, Mbjx, Scales=3, Methodx='coarse', Plotx=False):
    """MvMSEn  Returns the multivariate multiscale entropy of a multivariate dataset.
    
    .. code-block:: python
    
        MSx,CI = MvMSEn(Data, Mobj) 
    
    Returns a vector of multivariate multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequences in ``Data`` using the parameters specified 
    by the multiscale object (``Mobj``) over 3 temporal scales with coarse-
    graining (default). 
    
    .. caution::
 
        By default, the ``MvSampEn`` and ``MvFuzzEn`` multivariate entropy algorithms
        estimate entropy values using the "full"  method by comparing delay vectors 
        across all possible ``m+1`` expansions of the embedding space as applied in [1].
        These methods are **not** lower-bounded to 0, like most entropy algorithms,
        so ``MvMSEn`` may return negative entropy values if the base multivariate 
        entropy function is ``MvSampEn`` and ``MvFuzzEn``, even for stochastic processes...
    
    
    .. code-block:: python
    
        MSx,CI = MvMSEn(Data, Mobj, keyword = value, ...)
        
    Returns a vector of multivariate multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequences in ``Data`` using the parameters specified by
    the multiscale object (``Mobj``) and the following ``keyword`` arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :Methodx:  - Graining method, one of the following: [default: ``'coarse'``]  {``'coarse'``, ``'modified'``, ``'generalized'``}                        
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    For further info on these graining procedures see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``MSobject``, ``cMvMSEn``, ``MvFuzzEn``, ``MvSampEn``, ``MvPermEn``, ``MvCoSiEn``,  ``MvDispEn``
    
    :References:
        [1] Ahmed Mosabber Uddin, Danilo P. Mandic
             "Multivariate multiscale entropy analysis."
             IEEE signal processing letters 19.2 (2011): 91-94.
        
        [2] Madalena Costa, Ary Goldberger, and C-K. Peng,
             "Multiscale entropy analysis of complex physiologic time series."
             Physical review letters
             89.6 (2002): 068102.
        
        [3] Vadim V. Nikulin, and Tom Brismar,
             "Comment on “Multiscale entropy analysis of complex physiologic
             time series”." 
             Physical Review Letters 
             92.8 (2004): 089803.
        
        [4] Madalena Costa, Ary L. Goldberger, and C-K. Peng. 
             "Costa, Goldberger, and Peng reply." 
             Physical Review Letters
             92.8 (2004): 089804.
        
        [5] Madalena Costa, Ary L. Goldberger and C-K. Peng,
             "Multiscale entropy analysis of biological signals." 
             Physical review E 
             71.2 (2005): 021906.
        
        [6] Ranjit A. Thuraisingham and Georg A. Gottwald,
             "On multiscale entropy analysis for physiological data."
             Physica A: Statistical Mechanics and its Applications
             366 (2006): 323-332.
        
        [7] Ahmed Mosabber Uddin, Danilo P. Mandic
             "Multivariate multiscale entropy: A tool for complexity
             analysis of multichannel data."
             Physical Review E 84.6 (2011): 061918.
    
    """
    
    Mobj = deepcopy(Mbjx)
    Chk = ['coarse','modified','generalized']    
    
    Data = np.squeeze(Data)
    assert Data.shape[0]>10 and Data.ndim==2 and Data.shape[1]>1,  "Data:   must be an NxM numpy matrix where N>10 and M>1"
    N, Dn = Data.shape     
    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
                        object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert Methodx.lower() in Chk, "Methodx:  must be one of the following string names- \
                        'coarse', 'modified' , 'generalized'"    
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[:2] == 'Mv', ("Base entropy estimator must be a multivariate entropy method." 
    "To perform univariate multiscale entropy estimation, use MSEn().")
       
    Func2 = globals()[Methodx.lower()]
    MSx = np.zeros(Scales)
    
    for T in range(1,Scales+1):
        print(' .', end='')
        Temp = Func2(Data, T, Dn)  
        Tempx = Mobj.Func(Temp,**Mobj.Kwargs)[0]                                        
        MSx[T-1] = np.mean(Tempx)
            
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')

    if Plotx:
       figure()
       ax1 = axes()   
       ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
       ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
       ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_title('Multivariate Multiscale %s (%s-graining method)'%(Mobj.Func.__name__[2:], Methodx), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI


def coarse(Z, sx, Dn):
    Ns = Z.shape[0]//sx
    Y = np.zeros((Ns,Dn))
    for k in range(Dn):
        Y[:,k] = np.mean(np.reshape(Z[:sx*Ns,k],(Ns,sx)),axis=1)
    return Y

def modified(Z, sx, Dn):       
    Y = np.zeros((Z.shape[0]-sx+1,Dn))
    for k in range(Dn):
        Y[:,k] = np.convolve(Z[:,k],np.ones(sx),'valid')/sx
    return Y 

def generalized(Z, sx, Dn):
    Ns = Z.shape[0]//sx
    Y = np.zeros((Ns,Dn))
    for k in range(Dn):
        Y[:,k] = np.var(np.reshape(Z[:sx*Ns, k],(Ns,sx)), axis=1)
    return Y
    

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