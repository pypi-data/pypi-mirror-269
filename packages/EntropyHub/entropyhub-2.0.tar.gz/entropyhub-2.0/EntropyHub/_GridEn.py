"""Base Gridded Distribution Entropy function."""
import numpy as np     
import matplotlib.pyplot as mpl

def GridEn(Sig, m=3, tau=1, Logx=np.exp(1), Plotx=False):
    """GridEn  estimates the gridded distribution entropy of a univariate data sequence.
 
    .. code-block:: python
    
        GDE, GDR, _ = GridEn(Sig) 
        
    Returns the gridded distribution entropy (``GDE``) and the gridded 
    distribution rate (``GDR``) estimated from the data sequence (``Sig``) using 
    the default  parameters: grid coarse-grain = 3, time delay = 1, logarithm = base 2
   
    .. code-block:: python
    
        GDE, GDR, PIx, GIx, SIx, AIx = GridEn(Sig, keyword = value)
    
    Returns the gridded distribution entropy (``GDE``) estimated from the data 
    sequence (``Sig``) using the specified 'keyword' arguments:
        :m:     - Grid coarse-grain (m x m sectors), an integer > 1
        :tau:   - Time Delay, a positive integer
        :Logx:  - Logarithm base, a positive scalar
        :Plotx: - When ``Plotx == True``, returns gridded Poicaré plot and a bivariate histogram of the grid point distribution (default: False)  
    
    :See also:
        ``PhasEn``, ``CoSiEn``, ``SlopEn``, ``BubbEn``, ``MSEn``
    
    :References:
        [1] Chang Yan, et al.,
            "Novel gridded descriptors of poincaré plot for analyzing 
            heartbeat interval time-series." 
            Computers in biology and medicine 
            109 (2019): 280-289.
    
        [2] Chang Yan, et al. 
            "Area asymmetry of heart rate variability signal." 
            Biomedical engineering online 
            16.1 (2017): 1-14.
    
        [3] Alberto Porta, et al.,
            "Temporal asymmetries of short-term heart period variability 
            are linked to autonomic regulation." 
            American Journal of Physiology-Regulatory, Integrative and 
            Comparative Physiology 
            295.2 (2008): R550-R557.
    
        [4] C.K. Karmakar, A.H. Khandoker and M. Palaniswami,
            "Phase asymmetry of heart rate variability signal." 
            Physiological measurement 
            36.2 (2015): 303.

    """
 
    Sig = np.squeeze(Sig)  
       
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"
    assert isinstance(m,int) and (m > 1), "m:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Plotx,bool), "Plotx:     must be boolean - True or False"                          
        
    Sig_n = (Sig-min(Sig))/np.ptp(Sig)
    Temp = np.array([Sig_n[:-tau], Sig_n[tau:]])
    N, _, _ = np.histogram2d(Temp[0,:], Temp[1,:],m)
    Pj = np.flipud(np.transpose(N))/Temp.shape[1]
    Ppi = Pj[Pj>0]               
    if np.round(np.sum(Ppi)) != 1:
        print('WARNING: Potential error of estimated probabilities: P = %d'%np.sum(Ppi))
    
    GDE= -np.sum(Ppi*(np.log(Ppi)/np.log(Logx)))
    GDR = np.sum(np.sum(N!=0))/(m*m)
    
    with np.errstate(divide='ignore', invalid='ignore'):
        T2   = np.transpose(np.arctan(Temp[1,:]/Temp[0,:])*180/np.pi)
        Dup  = np.sum(abs(np.diff(Temp[:,T2>45],axis=0)))
        Dtot = np.sum(abs(np.diff(Temp[:,T2!=45],axis=0)))
        Sup  = np.sum((T2[T2>45]-45))
        Stot = np.sum(abs(T2[T2!=45]-45))
        Aup  = np.sum(abs(np.transpose(((T2[T2>45]-45))*np.sqrt(np.sum(Temp[:,T2>45]**2,axis=0)))))
        Atot = np.sum(abs(np.transpose(((T2[T2!=45]-45))*np.sqrt(np.sum(Temp[:,T2!=45]**2,axis=0)))))
        
        Index = {}
        Index['PIx'] = 100*sum(T2 < 45)/sum(T2!=45)
        Index['GIx'] = 100*Dup/Dtot
        Index['SIx'] = 100*Sup/Stot
        Index['AIx'] = 100*Aup/Atot

    if Plotx:

        ntrvl = np.linspace(0,1,m+1)
        mpl.subplots(1,2)
        x1 = mpl.subplot(121)
        ax1 =mpl.axes(x1)   
        
        ax1.plot(Sig_n[:-tau],Sig_n[tau:],'.m')
        ax1.plot(np.tile(ntrvl,(2,1)),np.array((np.zeros(m+1),np.ones(m+1))),'c')
        ax1.plot(np.array((np.zeros(m+1),np.ones(m+1))),np.tile(ntrvl,(2,1)),'c')
        ax1.plot([0, 1],[0, 1],'k') 
        ax1.set_aspect('equal', 'box')
        ax1.set_xlabel('X m')
        ax1.set_ylabel(r'$X m + \tau$') 
        ax1.set_xticks([0, 1])
        ax1.set_yticks([0, 1])
        ax1.set_xlim([0,1])
        ax1.set_ylim([0,1])

        x2 = mpl.subplot(122)
        ax2 = mpl.axes(x2)   
        # ax2.imshow(np.flipud(N), cmap='cool', aspect='equal')
        ax2.imshow(np.fliplr(N), cmap='cool', aspect='equal')
        ax2.set_xlabel('X m')
        ax2.set_ylabel(r'$X m + \tau$')
        ax2.set_xticks([])
        ax2.set_yticks([])
        mpl.show()
    
    return GDE, GDR, Index
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