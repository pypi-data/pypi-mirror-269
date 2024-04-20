"Base Multiscale Entropy function."
import numpy as np   
from PyEMD import EMD
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy
# from scipy.stats import moment

def MSEn(Sig, Mbjx, Scales=3, Methodx='coarse', RadNew=0, Plotx=False):
    """MSEn  Returns the multiscale entropy of a univariate data sequence.
    
    .. code-block:: python
    
        MSx,CI = MSEn(Sig, Mobj) 
    
    Returns a vector of multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequence ``Sig`` using the parameters specified 
    by the multiscale object (``Mobj``) over 3 temporal scales with coarse-
    graining (default). 
  
    .. code-block:: python
    
        MSx,CI = MSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequence ``Sig`` using the parameters specified by
    the multiscale object (``Mobj``) and the following ``keyword`` arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :Methodx:  - Graining method, one of the following: [default: ``'coarse'``]  {``'coarse'``, ``'modified'``, ``'imf'`` , ``'timeshift'`` , ``'generalized'``}
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn`` or ``ApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                         
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    For further info on these graining procedures see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``MSobject``, ``rMSEn``, ``cMSEn``, ``hMSEn``, ``XMSEn``, ``cXMSEn``, ``hXMSEn``, ``SampEn``
    
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
    
        [4] Madalena Costa, Ary L. Goldberger and C-K. Peng,
            "Multiscale entropy analysis of biological signals." 
            Physical review E 
            71.2 (2005): 021906.
    
        [5] Ranjit A. Thuraisingham and Georg A. Gottwald,
            "On multiscale entropy analysis for physiological data."
            Physica A: Statistical Mechanics and its Applications
            366 (2006): 323-332.
    
        [6] Meng Hu and Hualou Liang,
            "Intrinsic mode entropy based on multivariate empirical mode
            decomposition and its application to neural data analysis." 
            Cognitive neurodynamics
            5.3 (2011): 277-284.
    
        [7] Anne Humeau-Heurtier 
            "The multiscale entropy algorithm and its variants: A review." 
            Entropy 
            17.5 (2015): 3110-3123.
    
        [8] Jianbo Gao, et al.,
            "Multiscale entropy analysis of biological signals: a 
            fundamental bi-scaling law." 
            Frontiers in computational neuroscience 
            9 (2015): 64.
    
        [9] Paolo Castiglioni, et al.,
            "Multiscale Sample Entropy of cardiovascular signals: Does the
            choice between fixed-or varying-tolerance among scales 
            influence its evaluation and interpretation?." 
            Entropy
            19.11 (2017): 590.
    
        [10] Tuan D Pham,
            "Time-shift multiscale entropy analysis of physiological 
            signals." 
            Entropy 
            19.6 (2017): 257.
    
        [11] Hamed Azami and Javier Escudero,
            "Coarse-graining approaches in univariate multiscale sample 
            and dispersion entropy." 
            Entropy 20.2 (2018): 138.
            
        [12] Madalena Costa and Ary L. Goldberger,
            "Generalized multiscale entropy analysis: Application to quantifying 
            the complex volatility of human heartbeat time series." 
            Entropy 17.3 (2015): 1197-1203.
    
    """
    
    Mobj = deepcopy(Mbjx)
    
    Sig = np.squeeze(Sig)    
    Chk = ['coarse','modified','imf','timeshift','generalized']    
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert Methodx.lower() in Chk, "Methodx:  must be one of the following string names- \
    'coarse', 'modified' , 'imf', 'timeshift', 'generalized'"    
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['SampEn','ApEn']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'SampEn' or 'ApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[0].lower() != 'x', ("Base entropy estimator is a cross-entropy method." 
    "To perform multiscale CROSS-entropy estimation, use XMSEn.")
    
    if Mobj.Func.__name__ in 'SampEn': Mobj.Kwargs['Vcp'] = False 
    
    if Methodx.lower()=='imf':
        #EMD(total_power_thr=20)
        EMD().FIXE = 100
        EMD().FIXE_H = 100
        Sig = EMD().emd(Sig,max_imf=Scales-1)    
        assert Sig.shape[0]==Scales

    Func2 = globals()[Methodx.lower()]
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

    for T in range(1,Scales+1):
        print(' .', end='')
        Temp = Func2(Sig,T)        
        if Methodx.lower() == 'timeshift':
            Tempx = np.zeros(T)
            for k in range(T):
                if RadNew > 0:
                    Mobj.Kwargs.update({'r': Cx*Rnew(Temp[k,:])})                                    
                Tempy = Mobj.Func(Temp[k,:],**Mobj.Kwargs)
                
                if isinstance(Tempy,tuple):
                    if isinstance(Tempy[0],(int,float)):
                        Tempx[k] = Tempy[0]
                    else:
                        Tempx[k] =Tempy[0][-1]
                elif isinstance(Tempy,(int,float)):
                    Tempx[k] = Tempy
                elif isinstance(Tempy,np.ndarray):
                    Tempx[k] = Tempy[-1]
            
            Temp2 = np.mean(Tempx)
            
        else:
            if RadNew > 0:
                Mobj.Kwargs.update({'r': Cx*Rnew(Temp)})            
            Tempx = Mobj.Func(Temp,**Mobj.Kwargs)
                        
            if isinstance(Tempx,tuple):
                if isinstance(Tempx[0],(int,float)):
                    Temp2 = Tempx[0]
                else:
                    Temp2 =Tempx[0][-1]
            elif isinstance(Tempx,(int,float)):
                Temp2 = Tempx
            elif isinstance(Tempx,np.ndarray):
                Temp2 = Tempx[-1]
                    
        MSx[T-1] = Temp2
            
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
       ax1.set_title('Multiscale %s (%s-graining method)'%(Mobj.Func.__name__,Methodx), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI


def coarse(Z,sx):
    Ns = len(Z)//sx
    Y = np.mean(np.reshape(Z[:sx*Ns],(Ns,sx)),axis=1)
    return Y

def modified(Z,sx):
    # Ns = len(Z) - sx +1
    # Y = np.zeros(Ns)
    # for k in range(Ns):
    #     Y[k] = np.mean(Z[k:k+sx])
    
    Y = np.convolve(Z,np.ones(sx),'valid')/sx
    return Y 

def imf(Z,sx):
    Y = np.squeeze(np.sum(Z[:sx,:],axis=0))
    return Y

def timeshift(Z,sx):
    Y = np.transpose(np.reshape(Z[:sx*(len(Z)//sx)],(len(Z)//sx,sx)))
    return Y

def generalized(Z,sx):
    Ns = len(Z)//sx
    Y = np.var(np.reshape(Z[:sx*Ns],(Ns,sx)), axis=1)
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