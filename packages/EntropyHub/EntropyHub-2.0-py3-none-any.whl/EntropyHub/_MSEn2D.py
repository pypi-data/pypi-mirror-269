"Base Multiscale Bidimensional Entropy function."
import numpy as np   
from matplotlib.pyplot import figure, axes, show
from copy import deepcopy
from scipy.signal import convolve2d 

def MSEn2D(Mat, Mbjx, Scales=3, Methodx='coarse', RadNew=0, Plotx=False):
    """MSEn2D  Returns the multiscale entropy of a bidimensional data matrix.
    
    .. code-block:: python
    
        MSx,CI = MSEn(Mat, Mobj) 
    
    Returns a vector of multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data matrix ``Mat`` using the parameters specified 
    by the multiscale object (``Mobj``) over 3 temporal scales with coarse-
    graining (default). 
  
    .. code-block:: python
    
        MSx,CI = MSEn(Mat, Mobj, keyword = value, ...)
        
    Returns a vector of multiscale entropy values (``MSx``) and the complexity 
    index (``CI``) of the data matrix ``Mat`` using the parameters specified by
    the multiscale object (``Mobj``) and the following ``keyword`` arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :Methodx:  - Graining method, one of the following: [default: ``'coarse'``]  {``'coarse'``, ``'modified'``}
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn2D``, RadNew rescales the radius threshold in each sub-matrix
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                         
        :Plotx:    - When ``Plotx == True``, returns a plot of the entropy value at each time scale (i.e. the multiscale entropy curve) [default: False]
    
    For further info on these graining procedures see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``MSobject``, ``SampEn2D``, ``DispEn2D``, ``FuzzEn2D``, ``DistEn2D``, ``PermEn2D``, ``EspEn2D``
    
    :References:
         [1] Luiz E.V. Silva, et al.,
              "Two-dimensional multiscale entropy analysis: Applications to image texture evaluation."
              Signal Processing
              147 (2018): 224-232.
    
         [2] Cristina Morel and Anne Humeau-Heurtier
              "Multiscale permutation entropy for two-dimensional patterns." 
              Pattern Recognition Letters 
              150 (2021): 139-146.
    
         [3] Mirvana Hilal and Anne Humeau-Heurtier
              "Bidimensional Fuzzy Entropy: Principle Analysis and Biomedical Applications"
              IEEE Engineering in Medicine and Biology Society (EMBS) Conference
              2019: 4811-4814
    
    """
    
    Mobj = deepcopy(Mbjx)
    
    Mat = np.squeeze(Mat)    
    Chk = ['coarse','modified']    
    assert Mat.ndim==2 and min(Mat.shape)>10 , "Mat:   must be a 2D numpy array with height & width > 10"
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert Methodx.lower() in Chk, "Methodx:  must be one of the following string names - 'coarse', 'modified'"    
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) \
                and Mobj.Func.__name__ in ['SampEn2D']) or RadNew==0, \
    "RadNew:     must be 0, or an integer in range [1 4] with entropy function 'SampEn2D'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
        
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
        Temp = Func2(Mat,T)        
        
        if RadNew > 0:
            Mobj.Kwargs.update({'r': Cx*Rnew(Temp)})            
        Tempx = Mobj.Func(Temp,**Mobj.Kwargs)
                    
        if isinstance(Tempx,tuple):
           Temp2 = Tempx[0]  
        else:
           Temp2 = Tempx
                    
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
    Nh = Z.shape[0]//sx
    Nw = Z.shape[1]//sx    
    Y = np.mean(np.reshape(Z[:sx*Nh,:sx*Nw],(sx,Nh,sx,Nw)),axis=(0,2))
    return Y

def modified(Z,sx):
    Y = convolve2d(Z, np.ones((sx,sx)), mode='valid')/(sx*sx)
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