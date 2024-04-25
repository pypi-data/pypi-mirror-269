"Base refined Multiscale Entropy function."
import numpy as np   
from scipy.signal import butter, filtfilt
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def rMSEn(Sig, Mbjx, Scales=3, F_Order=6, F_Num=.5, RadNew=0, Plotx=False):
    """rMSEn  returns the refined multiscale entropy of a univariate data sequence.

    .. code-block::
        
        MSx, CI = rMSEn(Sig, Mobj) 
        
    Returns a vector of refined multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequence (``Sig``) using the parameters specified by
    the multiscale object (``Mobj``) and the following default parameters:
    Scales = 3, Butterworth LPF Order = 6, Butterworth LPF cutoff frequency
    at scale (T): Fc = 0.5/T. 
    If the entropy function specified by ``Mobj`` is ``SampEn`` or ``ApEn``, ``rMSEn``
    updates the threshold radius of the data sequence (Xt) at each scale
    to 0.2*std(Xt) if no ``r`` value is provided by Mobj, or r*std(Xt) if ``r``
    is specified.
     
    .. code-block:: python
    
        MSx, CI = rMSEn(Sig, Mobj, keyword = value, ...)
        
    Returns a vector of refined multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data sequence (``Sig``) using the parameters specified by
    the multiscale object (``Mobj``) and the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, a positive integer   (default: 3)
        :F_Order:  - Butterworth low-pass filter order, a positive integer (default: 6)
        :F_Num:    - Numerator of Butterworth low-pass filter cutoff frequency, a scalar value in range [0 < ``F_Num`` < 1].  The cutoff frequency  at each scale (T) becomes: Fc = F_Num/T.  (default: 0.5)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn`` or ``ApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``MSEn``, ``cMSEn``, ``hMSEn``, ``XMSEn``, ``rXMSEn``, ``SampEn``, ``ApEn``
    
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
    
        [4] José Fernando Valencia, et al.,
            "Refined multiscale entropy: Application to 24-h holter 
            recordings of heart period variability in healthy and aortic 
            stenosis subjects." 
            IEEE Transactions on Biomedical Engineering 
            56.9 (2009): 2202-2213.
    
        [5] Puneeta Marwaha and Ramesh Kumar Sunkaria,
            "Optimal selection of threshold value ‘r’for refined multiscale
            entropy." 
            Cardiovascular engineering and technology 
            6.4 (2015): 557-576.
    
    """

    Mobj = deepcopy(Mbjx)    
    Sig = np.squeeze(Sig)    
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(F_Order, int) and F_Order>0, \
    "F_Order:    a positive integer"
    assert isinstance(F_Num,float) and 0<F_Num<1, \
    "F_Num:     a scalar value in range [0 < F_Num < 1]"
    assert (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['SampEn','ApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'SampEn' or 'ApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[0].lower() != 'x', ("Base entropy estimator is a cross-entropy method." 
    "To perform refined multiscale CROSS-entropy estimation, use rXMSEn.")
    
    MSx = np.zeros(Scales)    
    if (Mobj.Func.__name__ in ['SampEn','ApEn']) and RadNew==0:
        RadNew = 1
    
    if Mobj.Func.__name__ in 'SampEn': Mobj.Kwargs['Vcp'] = False 
    
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
        Temp = refined(Sig,T,F_Order,F_Num)   
        if RadNew > 0:
            Mobj.Kwargs.update({'r': Cx*Rnew(Temp)})             
        Tempx = Mobj.Func(Temp,**Mobj.Kwargs)        
        
        if isinstance(Tempx,tuple):
            if isinstance(Tempx[0],(int,float)):
                MSx[T-1] = Tempx[0]
            else:
                MSx[T-1] =Tempx[0][-1]
        elif isinstance(Tempx,(int,float)):
                MSx[T-1] = Tempx
        elif isinstance(Tempx,np.ndarray):
                MSx[T-1] = Tempx[-1]
                    
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
       ax1.set_title('Refined Multiscale %s'%(Mobj.Func.__name__), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI

def refined(Z,sx,P1,P2):
    bb, aa = butter(P1, P2/sx)
    Yt = filtfilt(bb, aa, Z)
    Y = Yt[::sx]
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