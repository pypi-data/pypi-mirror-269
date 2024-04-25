"Base cross-Multiscale Entropy function."
import numpy as np 
from PyEMD import EMD
from matplotlib.pyplot import figure, axes,show
from copy import deepcopy

def XMSEn(Sig1, Sig2, Mbjx, Scales=3, Methodx='coarse', RadNew=0, Plotx=False):
    """XMSEn  returns the multiscale cross-entropy between two univariate data sequences.
 
    .. code-block:: python
    
        MSx, CI = XMSEn(Sig1, Sig2, Mobj) 
        
    Returns a vector of multiscale cross-entropy values (``MSx``) and the
    complexity index (``CI``) between the data sequences contained in ``Sig1`` and ``Sig2`` using 
    the parameters specified by the multiscale object (``Mobj``) over 3 temporal
    scales with coarse-graining (default).
     
    .. code-block:: python
    
        MSx, CI = XMSEn(Sig1, Sig2, Mobj, keyword = value, ...)
        
    Returns a vector of multiscale cross-entropy values (``MSx``) and the
    complexity index (``CI``) between the data sequences contained in ``Sig1`` and ``Sig2`` 
    using the parameters specified by the multiscale object (``Mobj``) and the
    following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1  [default: 3]
        :Methodx:  - Graining method, one of the following: [default: ``'coarse'``]  {``'coarse'``, ``'modified'``, ``'imf'`` , ``'timeshift'``, ``'generalized'``}
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Pooled Standard Deviation   - ``r*std(Ykj)``
                        * [2] Pooled Variance             - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve)  [default: False]
    
    :See also:
        ``MSobject``, ``XSampEn``, ``XApEn``, ``rXMSEn``, ``cXMSEn``, ``hXMSEn``, ``MSEn``
    
    :References:
        [1] Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
    
        [2] Madalena Costa, Ary Goldberger, and C-K. Peng,
            "Multiscale entropy analysis of complex physiologic time series."
            Physical review letters
            89.6 (2002): 068102.
    
        [3] Vadim V. Nikulin, and Tom Brismar,
            "Comment on “Multiscale entropy analysis of complex physiologic
            time series”." 
            Physical review letters 
            92.8 (2004): 089803.
    
        [4] Madalena Costa, Ary L. Goldberger, and C-K. Peng. 
            "Costa, Goldberger, and Peng reply." 
            Physical Review Letters
            92.8 (2004): 089804.
    
        [5] Antoine Jamin, et al,
            "A novel multiscale cross-entropy method applied to navigation 
            data acquired with a bike simulator." 
            41st annual international conference of the IEEE EMBC
            IEEE, 2019.
    
        [6] Antoine Jamin and Anne Humeau-Heurtier. 
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

    Chk = ['coarse','modified','imf','timeshift','generalized']  
    assert N1>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"  
    assert isinstance(Mobj,object) and Mobj.Func.__name__[0]=='X', "Mobj:  must \
    be a x-multiscale entropy object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert Methodx.lower() in Chk, "Methodx:  must be one of the following string names- \
    'coarse', 'modified' , 'imf', 'timeshift', 'generalized'"    
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['XSampEn','XApEn']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'XSampEn' or 'XApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
            
    if Mobj.Func.__name__ in 'XSampEn': Mobj.Kwargs['Vcp'] = False 
    
    if Methodx.lower()=='imf':
        EMD().FIXE = 100
        EMD().FIXE_H = 100
        S1 = EMD().emd(S1,max_imf=Scales-1).T    
        S2 = EMD().emd(S2,max_imf=Scales-1).T   

    Func2 = globals()[Methodx.lower()]
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
        Temp = Func2(S1,S2,T)  
        
        if Methodx.lower() == 'timeshift':
            Tempx = np.zeros(T)
            for k in range(T):
                print(' .', end='')
                if RadNew > 0:
                    Mobj.Kwargs.update({'r': Cx*Rnew(Temp[0][k,:],Temp[1][k,:])})                                    
                Tempy = Mobj.Func(Temp[0][k,:],Temp[1][k,:],**Mobj.Kwargs)
                
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
                    Mobj.Kwargs.update({'r': Cx*Rnew(Temp[0],Temp[1])})            
            Tempx = Mobj.Func(Temp[0],Temp[1],**Mobj.Kwargs)
            
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
    
    print('\n')
    if Plotx:
       figure()
       ax1 = axes()            
       ax1.plot(np.arange(1,Scales+1), MSx, color=(8/255, 63/255, 77/255), linewidth=3)
       ax1.scatter(np.arange(1,Scales+1), MSx, 60, color=(1,0,1))
       ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
       ax1.set_title('Cross-Multiscale %s (%s-graining method)'%(Mobj.Func.__name__,Methodx), 
                     fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))      
       show()
    
    return MSx, CI

def coarse(Za,Zb,sx):
    Na = len(Za)//sx
    Nb = len(Zb)//sx
    T1 = np.mean(np.reshape(Za[:sx*Na],(Na,sx)),axis=1)
    T2 = np.mean(np.reshape(Zb[:sx*Nb],(Nb,sx)),axis=1)
    return T1, T2

def modified(Za,Zb,sx):    
    T1 = np.convolve(Za,np.ones(sx),'valid')/sx
    T2 = np.convolve(Zb,np.ones(sx),'valid')/sx
    return T1, T2

def timeshift(Za,Zb,sx):
    # Y = np.zeros((sx,len(Z)//sx,2))
    # Y[:,:,0] = np.reshape(Z[:sx*(len(Z)//sx),0],(len(Z)//sx,sx)).transpose()
    # Y[:,:,1] = np.reshape(Z[:sx*(len(Z)//sx),1],(len(Z)//sx,sx)).transpose()   
    
    T1 = np.zeros((sx,len(Za)//sx))
    T2 = np.zeros((sx,len(Zb)//sx))
    T1 = np.reshape(Za[:sx*(len(Za)//sx)],(len(Za)//sx,sx)).T
    T2 = np.reshape(Zb[:sx*(len(Zb)//sx)],(len(Zb)//sx,sx)).T   
    return T1, T2

def generalized(Za,Zb,sx):
    Na = len(Za)//sx
    Nb = len(Zb)//sx
    T1 = np.var(np.reshape(Za[:sx*Na],(Na,sx)),axis=1)
    T2 = np.var(np.reshape(Zb[:sx*Nb],(Nb,sx)),axis=1)
    return T1, T2

def imf(Za,Zb,sx):
    # Y = np.squeeze(np.sum(Z[:,:,:sx],axis=2))    
    T1 = np.squeeze(np.sum(Za[:,:sx],axis=1))
    T2 = np.squeeze(np.sum(Zb[:,:sx],axis=1))
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