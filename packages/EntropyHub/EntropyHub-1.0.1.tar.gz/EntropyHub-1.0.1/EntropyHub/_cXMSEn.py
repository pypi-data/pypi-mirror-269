"Base composite cross-Multiscale Entropy function."
import numpy as np  
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def cXMSEn(Sig1, Sig2, Mbjx,  Scales=3, RadNew=0, Refined=False, Plotx=False):
    """cXMSEn  returns the composite (or refined-composite) multiscale cross-entropy between two univariate data sequences.
 
    .. code-block:: python
        
        MSx, CI = cXMSEn(Sig1, Sig2, Mobj) 
        
    Returns a vector of composite multiscale cross-entropy values (``MSx``) 
    between two univariate data sequences contained in ``Sig1`` and ``Sig2`` using the 
    parameters specified by the multiscale object (``Mobj``) using the composite 
    multiscale method (cMSE) over 3 temporal scales.
    
    .. code-block:: python 
        
        MSx, CI = cXMSEn(Sig1, Sig2, Mobj, Refined = True) 
        
    Returns a vector of refined-composite multiscale cross-entropy values (``MSx``) for the data 
    sequences (``Sig1``, ``Sig2``) using the parameters specified by the multiscale object 
    (``Mobj``) using the refined-composite multiscale entropy method (rcMSE) over 3 temporal
    scales. When ``Refined == True``, the base entropy method must be ``XSampEn`` or ``XFuzzEn``.
    If the entropy method is ``XSampEn``, cXMSEn employs the method described in [7]. 
    If the entropy method is ``XFuzzEn``, cXMSEn employs the method described in [8].    
     
    .. code-block:: python
        
        MSx, CI = cXMSEn(Sig1, Sig2, Mobj, keyword = value, ...)
        
    Returns a vector of composite multiscale cross-entropy values (``MSx``) 
    between the data sequences contained in ``Sig1`` and ``Sig2`` using the parameters
    specified by the multiscale object (Mobj) and the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Pooled Standard Deviation   - ``r*std(Ykj)``
                        * [2] Pooled Variance             - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Refined:  - Refined-composite XMSEn method. When ``Refined == True`` and the cross-entropy function specified by
                    ``Mobj`` is ``XSampEn`` or ``XFuzzEn``,  ``cXMSEn`` returns the refined-composite multiscale entropy (rcXMSEn) [default: False]
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``XMSEn``, ``rXMSEn``, ``hXMSEn``, ``XSampEn``, ``XApEn``, ``MSEn``, ``cMSEn``, ``rMSEn``
    
    :References:
        [1] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
    
        [2] Yi Yin, Pengjian Shang, and Guochen Feng, 
            "Modified multiscale cross-sample entropy for complex time 
            series."
            Applied Mathematics and Computation 
            289 (2016): 98-110.
    
        [3] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
    
        [4] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
    
        [5] Antoine Jamin and Anne Humeau-Heurtier. 
            "(Multiscale) Cross-Entropy Methods: A Review." 
            Entropy 
            22.1 (2020): 45.
    
        [6] Shuen-De Wu, et al.,
            "Time series analysis using composite multiscale entropy." 
            Entropy 
            15.3 (2013): 1069-1084.
            
        [7] Shuen-De Wu, et al.,
            "Analysis of complex time series using refined composite 
            multiscale entropy." 
            Physics Letters A 
            378.20 (2014): 1369-1374.
            
        [8] Hamed Azami et al.,
            "Refined multiscale fuzzy entropy based on standard deviation 
            for biomedical signal analysis"
            Med Biol Eng Comput 
            55 (2017):2037–2052
    
    """
    
    Mobj = deepcopy(Mbjx)    
    S1 = np.squeeze(Sig1)
    S2 = np.squeeze(Sig2)
    assert Sig1.ndim==1 and Sig2.ndim==1,   "Sig1/Sig2:   must be numpy vectors (N>10)" 
    N1 = S1.shape[0]
    N2 = S2.shape[0]

    assert N1>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"     
    assert isinstance(Mobj,object) and Mobj.Func.__name__[0]=='X', "Mobj:  must \
    be a multiscale entropy object created with the function EntropyHub.MSobject \
        and the base estimator must be a CROSS-entropy method."    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(Refined, bool) and ((Refined==True and Mobj.Func.__name__ 
                    in ['XSampEn','XFuzzEn'])  or Refined==False), \
    "Refined:       must be a True or False. If Refined==True, Mobj.Func must be XSampEn or XFuzzEn"
    assert (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['XSampEn','XApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'XSampEn' or 'XApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
        
    MSx = np.zeros(Scales)       
    if RadNew > 0:
        if RadNew == 1:
            Rnew = lambda x,y: np.sqrt((np.var(x)*(len(x)-1) + np.var(y)*(len(y)-1))/(len(x)+len(y)-1))
        elif RadNew == 2:
            Rnew = lambda x,y: (np.var(x)*(len(x)-1) + np.var(y)*(len(y)-1))/(len(x)+len(y)-1)
        elif RadNew == 3:
            Rnew = lambda x,y: np.mean(abs(np.hstack((x,y))-np.mean(np.hstack((x,y)))))
        elif RadNew == 4:
            Rnew = lambda x,y: np.median(abs(np.hstack((x,y))-np.median(np.hstack((x,y)))))   
                
        try:
            Cx = Mobj.Kwargs.get('r')*1
        except:
            Cy = ['Pooled Standard Deviation','Pooled Variance','Joint Mean Abs Deviation', 'Joint Median Abs Deviation']
            print('WARNING: No radius value provided.\nDefault set to ' \
                  '0.2*(%s) of each new time-series.'%Cy[RadNew-1])              
            Cx = .2
                        
    if Mobj.Func.__name__ in 'XSampEn': Mobj.Kwargs['Vcp'] = False 

    if Refined and Mobj.Func.__name__ == 'XFuzzEn':
        Tx = 1
        if 'Logx' in Mobj.Kwargs.keys(): Logx = Mobj.Kwargs['Logx']
        else: Logx = np.e
        
    elif Refined and Mobj.Func.__name__ == 'XSampEn':
        Tx = 0
        if 'Logx' in Mobj.Kwargs.keys(): Logx = Mobj.Kwargs['Logx']
        else: Logx = np.e
    
    else:  Tx = 0
       
    for T in range(1,Scales+1):
        Temp = modified(S1, S2, T, Tx)
        
        N1 = T*(len(Temp[0])//T)
        N2 = T*(len(Temp[1])//T)
        
        Temp3 = np.zeros(T)
        Temp2 = np.zeros(T)
        
        for k in range(T):
            print(' .', end='')
            if RadNew > 0:
                Mobj.Kwargs.update({'r': Cx*Rnew(Temp[0][k:N1:T], Temp[1][k:N2:T])})    
                
            if Refined:
                _, Ma, Mb = Mobj.Func(Temp[0][k:N1:T],Temp[1][k:N2:T],**Mobj.Kwargs)
                Temp2[k] = Ma[-1]
                Temp3[k] = Mb[-1]
            else:
                Temp2 = Mobj.Func(Temp[0][k:N1:T],Temp[1][k:N2:T],**Mobj.Kwargs)
                
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
            MSx[T-1] = -np.log(sum(Temp2)/sum(Temp3))/np.log(Logx)
        elif Refined and Tx==1:
            MSx[T-1] = -np.log(sum(Temp3)/sum(Temp2))/np.log(Logx)
        else:
            MSx[T-1] = np.mean(Temp3)
    
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')
    
    print('\n')
            
    if Plotx == 1:
        if Refined:
            strx = 'Refined-Composite Cross-'
        else:
            strx = 'Composite Cross-'
        
        figure()
        ax1 = axes()   
        ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
        ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
        ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_title('%sMultiscale %s'%(strx,Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))       
        show()

    return MSx, CI

def modified(Za,Zb,sx,Tx):    
    if Tx==1:
        T1 = np.asarray([np.std(Za[x:x+sx]) for x in range(len(Za)-sx+1)])
        T2 = np.asarray([np.std(Zb[x:x+sx]) for x in range(len(Zb)-sx+1)])

    else: 
        T1 = np.convolve(Za,np.ones(sx),'valid')/sx
        T2 = np.convolve(Zb,np.ones(sx),'valid')/sx
    
    return T1, T2


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