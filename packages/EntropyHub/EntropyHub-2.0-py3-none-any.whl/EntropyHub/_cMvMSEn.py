"Base Composite / Refined-Composite Multivariate Multiscale Entropy function."
import numpy as np   
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy
# from scipy.stats import moment

def cMvMSEn(Data, Mbjx, Scales=3, Refined=False, Plotx=False):
    """cMvMSEn  Returns the composite + refined-composite multivariate multiscale entropy of a multivariate dataset.
    
    .. code-block:: python
    
        MSx,CI = cMvMSEn(Data, Mobj) 
    
    Returns a vector of composite multivariate multiscale entropy values (``MSx``) and the complexity 
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
        
        MSx, CI = cMvMSEn(Data, Mobj, Refined = True) 
        
    Returns a vector of refined-composite multiscale entropy values (``MSx``) for the data 
    sequences in (``Data``) using the parameters specified by the multiscale object 
    (``Mobj``) using the refined-composite multivariate multiscale entropy method (rcMSE) over 3 temporal
    scales. When ``Refined == True``, the base entropy method must be ``MvSampEn`` or ``MvFuzzEn``.
    If the entropy method is ``MvSampEn``, cMvMSEn employs the method described in [1]. 
    If the entropy method is ``MvFuzzEn``, cMvMSEn employs the method described in [5]. 

    .. code-block:: python
    
        MSx,CI = cMvMSEn(Data, Mobj, keyword = value, ...)
        
    Returns a vector of composite multivariate multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequences in ``Data`` using the parameters specified by
    the multiscale object (``Mobj``) and the following ``keyword`` arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :Refined:  - Refined-composite MvMSEn method. When ``Refined == True`` and the entropy function specified by ``Mobj`` is ``MvSampEn`` or ``MvFuzzEn``, ``cMvMSEn`` returns the refined-composite multivariate multiscale entropy (rcMSEn) [default: False]
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    For further info on these graining procedures see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``MSobject``, ``MvMSEn``, ``MvFuzzEn``, ``MvSampEn``, ``MvPermEn``, ``MvCoSiEn``,  ``MvDispEn``
    
    :References:
        [1] Shuen-De Wu, et al.,
              "Time series analysis using composite multiscale entropy."
              Entropy
              15.3 (2013): 1069-1084.
    
        [2] Shuen-De Wu, et al.,
              "Analysis of complex time series using refined composite
              multiscale entropy."
              Physics Letters A
              378.20 (2014): 1369-1374.
    
        [3] Ahmed Mosabber Uddin, Danilo P. Mandic
              "Multivariate multiscale entropy: A tool for complexity
              analysis of multichannel data."
              Physical Review E 84.6 (2011): 061918.
    
        [4] Ahmed Mosabber Uddin, Danilo P. Mandic
              "Multivariate multiscale entropy analysis."
              IEEE signal processing letters 19.2 (2011): 91-94.
    
        [5] Azami, Alberto Fernández, Javier Escudero.
              "Refined multiscale fuzzy entropy based on standard deviation for
              biomedical signal analysis."
              Medical & biological engineering & computing 55 (2017): 2037-2052.
    
    """
    
    Mobj = deepcopy(Mbjx)    
    Data = np.squeeze(Data)
    assert Data.shape[0]>10 and Data.ndim==2 and Data.shape[1]>1,  "Data:   must be an NxM numpy matrix where N>10 and M>1"
    N, Dn = Data.shape     
    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
                        object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(Refined, bool) and ((Refined==True and Mobj.Func.__name__ in ['MvSampEn','MvFuzzEn'])
        or Refined==False), \
    "Refined:       must be a bool (True or False). If Refined==True, Mobj.Func must be MvSampEn or MvFuzzEn" 
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[:2] == 'Mv', ("Base entropy estimator must be a multivariate entropy method." 
    "To perform univariate multiscale entropy estimation, use MSEn().")
           
    if Refined:
        if  Mobj.Func.__name__== 'MvFuzzEn':      Tx = 1
        elif Mobj.Func.__name__ == 'MvSampEn':    Tx = 0
        
        if 'Logx' in Mobj.Kwargs.keys():   Logx = Mobj.Kwargs['Logx']
        else:   Logx = np.exp(1)
        
    else: 
        Tx = 0
  
    MSx = np.zeros(Scales)    
    for T in range(1,Scales+1):
        print(' .', end='')
        Temp = modified(Data, T, Tx, Dn)          
        N = T*(Temp.shape[0]//T)
        Ma = np.zeros(T)   
        Mb = np.zeros(T)     

        for k in range(T):        
            if Refined:  _, Ma[k], Mb[k], _ = Mobj.Func(Temp[k:N:T,:],**Mobj.Kwargs)
            else:   Ma[k] = Mobj.Func(Temp[k:N:T,:],**Mobj.Kwargs)[0]
    
        if Refined:
            MSx[T-1] = -np.log(np.sum(Mb)/np.sum(Ma))/np.log(Logx)
        else:
            MSx[T-1] = np.mean(Ma)       
                   
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')

    if Plotx:
        if Refined:
            strx = 'Refined-Composite'
        else:
            strx = 'Composite'
        
        figure()
        ax1 = axes()   
        ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
        ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
        ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_title('%s Multivariate Multiscale %s'%(strx,Mobj.Func.__name__[2:]), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))       
        show()
    
    return MSx, CI


def modified(Z, sx, Tx, Dn):    
    Ns = Z.shape[0]-sx+1
    Y = np.zeros((Ns,Dn))    
    if Tx==1:
        for k in range(Dn):
            Temp = [np.std(Z[x:x+sx,k]) for x in range(Ns)]
            Y[:,k] = np.array(Temp)
    
    else:
        for k in range(Dn):
            Y[:,k] = np.convolve(Z[:,k],np.ones(sx),'valid')/sx    
   
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