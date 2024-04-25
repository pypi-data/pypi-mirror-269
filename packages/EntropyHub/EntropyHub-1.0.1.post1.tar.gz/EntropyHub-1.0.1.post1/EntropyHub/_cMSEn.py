"Base composite Multiscale Entropy function."
import numpy as np 
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def cMSEn(Sig, Mbjx, Scales=3, RadNew=0, Refined=False, Plotx=False):
    """cMSEn  Returns the composite (or refined-composite) multiscale entropy of a univariate data sequence.

    .. code-block:: python 
        
        MSx, CI = cMSEn(Sig, Mobj) 
        
    Returns a vector of composite multiscale entropy values (``MSx``) for the data 
    sequence (``Sig``) using the parameters specified by the multiscale object 
    (``Mobj``) using the composite multiscale entropy method (cMSE) over 3 temporal
    scales. 
    
    .. code-block:: python 
        
        MSx, CI = cMSEn(Sig, Mobj, Refined = True) 
        
    Returns a vector of refined-composite multiscale entropy values (``MSx``) for the data 
    sequence (``Sig``) using the parameters specified by the multiscale object 
    (``Mobj``) using the refined-composite multiscale entropy method (rcMSE) over 3 temporal
    scales. When ``Refined == True``, the base entropy method must be ``SampEn`` or ``FuzzEn``.
    If the entropy method is ``SampEn``, cMSEn employs the method described in [5]. 
    If the entropy method is ``FuzzEn``, cMSEn employs the method described in [6].     
    
    .. code-block:: python
        
        MSx, CI = cMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of composite multiscale entropy values (``MSx``) of the 
    data sequence (``Sig``) using the parameters specified by the multiscale 
    object (``Mobj``) and the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn`` or ``ApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Refined:  - Refined-composite MSEn method. When ``Refined == True`` and the entropy function specified by ``Mobj`` is ``SampEn`` or ``FuzzEn``, 
                     ``cMSEn`` returns the refined-composite multiscale entropy (rcMSEn) [default: False]
        :Plotx:    - When Plotx == True, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``MSEn``, ``rMSEn``, ``hMSEn``, ``XMSEn``, ``cXMSEn``, ``SampEn``, ``ApEn`` 
     
    :References:
        [1] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
            
        [2] Vadim V. Nikulin, and Tom Brismar,
            "Comment on “Multiscale entropy analysis of complex physiologic
            time series”." 
            Physical review letters 
            92.8 (2004): 089803.
    
        [3] Madalena Costa, Ary L. Goldberger, and C-K. Peng. 
            "Costa, Goldberger, and Peng reply." 
            Physical Review Letters
            92.8 (2004): 089804.
    
        [4] Shuen-De Wu, et al.,
            "Time series analysis using composite multiscale entropy." 
            Entropy 
            15.3 (2013): 1069-1084.
    
        [5] Shuen-De Wu, et al.,
            "Analysis of complex time series using refined composite 
            multiscale entropy." 
            Physics Letters A 
            378.20 (2014): 1369-1374.
            
        [6] Hamed Azami et al.,
            "Refined multiscale fuzzy entropy based on standard deviation 
            for biomedical signal analysis"
            Med Biol Eng Comput 
            55 (2017):2037–2052

    
    """
  
    Mobj = deepcopy(Mbjx)    
    Sig = np.squeeze(Sig)    
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['SampEn','ApEn']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'SampEn' or 'ApEn'"
    assert isinstance(Refined, bool) and ((Refined==True and Mobj.Func.__name__ in ['SampEn','FuzzEn'])
        or Refined==False), \
    "Refined:       must be a bool (True or False). If Refined==True, Mobj.Func must be SampEn or FuzzEn"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[0].lower() != 'x', ("Base entropy estimator is a cross-entropy method." 
    "To perform composite multiscale CROSS-entropy estimation, use cXMSEn.")
    
    if Mobj.Func.__name__ in 'SampEn': Mobj.Kwargs['Vcp'] = False 
    
    MSx = np.zeros(Scales)    
    if RadNew > 0:
        if RadNew == 1:
            Rnew = lambda x: np.std(x)
        elif RadNew == 2:
            Rnew = lambda x: np.var(x)
        elif RadNew == 3:
            Rnew = lambda x: np.mean(abs(x-np.mean(x)))
        elif RadNew == 4:
            Rnew = lambda x: np.median(abs(x-np.median(x)))    
        
        try:
            Cx = Mobj.Kwargs.get('r')*1
        except:
            Cy = ['Standard Deviation','Variance','Mean Abs Deviation',
                  'Median Abs Deviation']
            print('WARNING: No radius value provided.\nDefault set to ' \
                  '0.2*(%s) of each new time-series.'%Cy[RadNew-1])            
            Cx = .2

    if Refined and Mobj.Func.__name__ == 'FuzzEn':
        Tx = 1
        if 'Logx' in Mobj.Kwargs.keys(): Logx = Mobj.Kwargs['Logx']
        else: Logx = np.e
        
    elif Refined and Mobj.Func.__name__ == 'SampEn':
        Tx = 0
        if 'Logx' in Mobj.Kwargs.keys(): Logx = Mobj.Kwargs['Logx']
        else: Logx = np.e

    else:  Tx = 0
    
    for T in range(1,Scales+1):
        Temp = modified(Sig,T,Tx)    
        
        N = T*(len(Temp)//T)
        Temp3 = np.zeros(T)
        Temp2 = np.zeros(T)                
        for k in range(T):        
            print(' .', end='')
            if RadNew > 0:
                Mobj.Kwargs.update({'r': Cx*Rnew(Temp[k::T])})       
                
            if Refined:
                _, Ma, Mb = Mobj.Func(Temp[k:N:T],**Mobj.Kwargs)
                Temp2[k] = Ma[-1]
                Temp3[k] = Mb[-1]
            else:
                Temp2 = Mobj.Func(Temp[k:N:T],**Mobj.Kwargs)
                if isinstance(Temp2,tuple):
                    if isinstance(Temp2[0],(int,float)):
                        Temp3[k] = Temp2[0]
                    else:
                        Temp3[k] = Temp2[0][-1]       
                elif isinstance(Temp2,(int,float)):
                    Temp3[k] = Temp2
                elif isinstance(Temp2,np.ndarray):
                    Temp3[k] = Temp2[-1]
                     
        if Refined and Tx==0:
            MSx[T-1] = -np.log(np.sum(Temp2)/np.sum(Temp3))/np.log(Logx)
        elif Refined and Tx==1:
            MSx[T-1] = -np.log(np.sum(Temp3)/np.sum(Temp2))/np.log(Logx)
        else:
            MSx[T-1] = np.mean(Temp3)
    
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
        ax1.set_title('%s Multiscale %s'%(strx,Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))       
        show()
    
    return MSx, CI

def modified(Z,sx, Tx):
    # Ns = len(Z) - sx +1
    # Y = np.zeros(Ns)
    # for k in range(Ns):
    #     Y[k] = np.mean(Z[k:k+sx])
    
    if Tx==1:
        Y = np.asarray([np.std(Z[x:x+sx]) for x in range(len(Z)-sx+1)])
    else: 
        Y = np.convolve(Z,np.ones(sx),'valid')/sx
        
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