"Base Refined Cross-Multiscale Entropy function."
import numpy as np 
from scipy.signal import butter, filtfilt
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy

def rXMSEn(Sig1, Sig2, Mbjx, Scales=3, F_Order=6, F_Num=.5, RadNew=0, Plotx=False):
    """rXMSEn  returns the refined multiscale cross-entropy between two   univariate data sequences.
            
    .. code-block:: python

        MSx, CI = rXMSEn(Sig1, Sig2, Mobj) 
        
    Returns a vector of refined multiscale cross-entropy values (``MSx``) and
    the complexity index (``CI``) between the data sequences contained in ``Sig1`` and ``Sig2``
    using the parameters specified by the multiscale object (``Mobj``) and the
    following default parameters:   Scales = 3, Butterworth LPF Order = 6, 
    Butterworth LPF cutoff frequency at scale (T): Fc = 0.5/T. 
    If the entropy function specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, ``rXMSEn``
    updates the threshold radius of the data sequences at each scale
    to 0.2*SDpooled(Sig1,Sig2) if no ``r`` value is provided by Mobj, or r*SDpooled(Sig1,Sig2) if ``r``
    is specified.
     
    .. code-block:: python
    
        MSx, CI = rXMSEn(Sig1, Sig2, Mobj, keyword = value, ...)
        
    Returns a vector of refined multiscale cross-entropy values (``MSx``) and 
    the complexity index (``CI``) between the data sequences contained in ``Sig1`` and ``Sig2`` 
    using the parameters specified by the multiscale object (``Mobj``) and the
    following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1 (default: 3)
        :F_Order:  - Butterworth low-pass filter order, a positive integer (default: 6)
        :F_Num:    - Numerator of Butterworth low-pass filter cutoff frequency, a scalar value in range [0 < ``F_Num`` < 1]. The cutoff frequency  at each scale (T) becomes: Fc = ``F_Num``/T.  (default: 0.5)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Pooled Standard Deviation   - ``r*std(Ykj)``
                        * [2] Pooled Variance             - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                        
        :Plotx:   - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    :See also:
        ``MSobject``, ``XMSEn``, ``cXMSEn``, ``hXMSEn``, ``XSampEn``, ``XApEn``, ``MSEn``, ``rMSEn``
      
    :References:
        [1] Matthew W. Flood,
            "rXMSEn - EntropyHub Project"
            2024, https://github.com/MattWillFlood/EntropyHub
      
        [2] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
      
        [3] José Fernando Valencia, et al.,
            "Refined multiscale entropy: Application to 24-h holter 
            recordings of heart period variability in healthy and aortic 
            stenosis subjects." 
            IEEE Transactions on Biomedical Engineering 
            56.9 (2009): 2202-2213.
      
        [4] Puneeta Marwaha and Ramesh Kumar Sunkaria,
            "Optimal selection of threshold value ‘r’ for refined multiscale
            entropy." 
            Cardiovascular engineering and technology 
            6.4 (2015): 557-576.
      
        [5] Yi Yin, Pengjian Shang, and Guochen Feng, 
            "Modified multiscale cross-sample entropy for complex time 
            series."
            Applied Mathematics and Computation 
            289 (2016): 98-110.
      
        [6] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
      
        [7] Antoine Jamin and Anne Humeau-Heurtier. 
            "(Multiscale) Cross-Entropy Methods: A Review." 
            Entropy 
            22.1 (2020): 45.
      
    """
    
    Mobj = deepcopy(Mbjx)    
    S1 = np.squeeze(Sig1)
    S2 = np.squeeze(Sig2)
    assert Sig1.ndim==1 and Sig2.ndim==1,   "Sig1/Sig2:   must be numpy vectors (N>10)" 
    N1 = S1.shape[0]
    N2 = S2.shape[0]
                   
    assert N1>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"     
    assert isinstance(Mobj,object) and Mobj.Func.__name__[0]=='X', "Mobj:  must \
    be a x-multiscale entropy object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(F_Order, int) and F_Order>0, "F_Order:  a positive integer"
    assert isinstance(F_Num,float) and 0<F_Num<1, "F_Num:  a scalar value in range [0 < F_Num < 1]"   
    assert (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['XSampEn','XApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'XSampEn' or 'XApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    
    if Mobj.Func.__name__ in 'XSampEn': Mobj.Kwargs['Vcp'] = False 
    
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

    for T in range(1,Scales+1):
        print(' .', end='')
        Temp = refined(S1,S2,T,F_Order,F_Num)
        if RadNew > 0:
            Mobj.Kwargs.update({'r': Cx*Rnew(Temp[0],Temp[1])})            
        Tempx = Mobj.Func(Temp[0],Temp[1],**Mobj.Kwargs)
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
    
    print('\n')

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


def refined(Za, Zb, sx, P1, P2):
    bb, aa = butter(P1, P2/sx)
    Ya = filtfilt(bb, aa, Za)
    Yb = filtfilt(bb, aa, Zb)
    T1 = Ya[::sx]
    T2 = Yb[::sx]    
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