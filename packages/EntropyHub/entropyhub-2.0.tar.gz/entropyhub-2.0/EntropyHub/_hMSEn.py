"Base heirarchical Multiscale Entropy function."
import numpy as np   
from matplotlib.pyplot import figure, show, subplot
import matplotlib.gridspec as gridspec
from copy import deepcopy

def hMSEn(Sig, Mbjx, Scales=3, RadNew=0, Plotx=False):
    """hMSEn  returns the hierarchical entropy of a univariate data sequence.
 
    .. code-block:: python
    
        MSx, Sn, CI = hMSEn(Sig, Mobj) 
        
    Returns a vector of entropy values (``MSx``) calculated at each node in the
    hierarchical tree, the average entropy value across all nodes at each 
    scale (``Sn``), and the complexity index (``CI``) of the hierarchical tree
    (i.e. ``sum(Sn)``) for the data sequence (``Sig``) using the parameters specified
    by the multiscale object (Mobj) over 3 temporal scales (default).
    The entropy values in MSx are ordered from the root node (S_00) to the
    Nth subnode at scale T (S_TN): i.e. S_00, S_10, S_11, S_20, S_21, S_22,
    S_23, S_30, S_31, S_32, S_33, S_34, S_35, S_36, S_37, S_40, ... , S_TN.
    The average entropy values in Sn are ordered in the same way, with the
    value of the root node given first: i.e. S0, S1, S2, ..., ST
     
    .. code-block:: python
    
        MSx, Sn, CI = hMSEn(Sig, Mobj, keyword = value, ...)
    
    Returns a vector of entropy values (``MSx``) calculated at each node in the
    hierarchical tree, the average entropy value across all nodes at each 
    scale (``Sn``), and the complexity index (``CI``) of the entire hierarchical
    tree for the data sequence (Sig) using the following 'keyword' arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default = 3)  At each scale (T), entropy is estimated for 2^(T-1) nodes.
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the entropy specified by ``Mobj`` is ``SampEn`` or ``ApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                         
                        * [1] Standard Deviation          - ``r*std(Ykj)``
                        * [2] Variance                    - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                     
        :Plotx:    - When ``Plotx == True``, returns a plot of the average entropy value at each time scale (i.e. the multiscale entropy curve) and a network graph showing the entropy value of each node in the hierarchical tree decomposition.  (default: False)
    
    :See also:
        ``MSobject``, ``MSEn``, ``rMSEn``, ``cMSEn``, ``XMSEn``, ``hXMSEn``, ``rXMSEn``, ``cXMSEn``
    
    :References:
        [1] Ying Jiang, C-K. Peng and Yuesheng Xu,
            "Hierarchical entropy analysis for biological signals."
            Journal of Computational and Applied Mathematics
            236.5 (2011): 728-742.
    
    """
    
    Mobj = deepcopy(Mbjx)    
    Sig = np.squeeze(Sig)    
    assert Sig.shape[0]>10 and Sig.ndim == 1, "Sig:   must be a numpy vector"    
    assert isinstance(Mobj,object), "Mobj:  must be a multiscale entropy \
    object created with the function EntropyHub.MSobject"    
    assert isinstance(Scales,int) and Scales>1, "Scales:    must be an integer > 1"
    assert isinstance(RadNew,int) and (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['SampEn','ApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'SampEn' or 'ApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
    assert Mobj.Func.__name__[0].lower() != 'x', ("Base entropy estimator is a cross-entropy method." 
    "To perform heirarchical multiscale CROSS-entropy estimation, use hXMSEn.")
    
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
    
    XX,N = Hierarchy(Sig,Scales)
    MSx = np.zeros(XX.shape[0])
    for T in range(XX.shape[0]):
        print(' .', end='')
        Temp = XX[T,:int(N/(2**(int(np.log2(T+1)))))]        
        if RadNew:
            Mobj.Kwargs.update({'r': Cx*Rnew(Temp)})            
        Temp2 = Mobj.Func(Temp,**Mobj.Kwargs)       
        
        if isinstance(Temp2,tuple):
            if isinstance(Temp2[0],(int,float)):
                MSx[T] = Temp2[0]
            else:
                MSx[T] =Temp2[0][-1]
        elif isinstance(Temp2,(int,float)):
            MSx[T] = Temp2
        elif isinstance(Temp2,np.ndarray):
            MSx[T] = Temp2[-1]
                                        
    Sn = np.zeros(Scales)
    for t in range(Scales):
        Sn[t] = np.mean(MSx[(2**t)-1:(2**(t+1))-1])
       
    CI = sum(MSx)
    if np.any(np.isnan(MSx)):
        print('Some entropy values may be undefined.')
    print('\n')
    
    if Plotx:
        
        figure()
        G = gridspec.GridSpec(10, 1)    
        ax1 = subplot(G[:2, :])
        ax1.plot(np.arange(1,Scales+1), Sn, color=(8/255, 63/255, 77/255), linewidth=3)
        ax1.scatter(np.arange(1,Scales+1), Sn, 60, color=(1,0,1))
        ax1.set_xlabel('Scale Factor',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_ylabel('Entropy Value',fontsize=12,fontweight='bold',color=(7/255, 54/255, 66/255))
        ax1.set_title('Hierarchical Multiscale %s Entropy'%(Mobj.Func.__name__), 
                      fontsize=16,fontweight='bold',color=(7/255, 54/255, 66/255))         

        N = 2**(Scales-1)
        x = np.zeros(2*N - 1,dtype=int)  
        x[0] = N;        
        y = Scales*(Scales - np.log2(np.arange(1,2*N))//1)
        for k in range(1,2*N):
            Q = int(np.log2(k)//1)
            P = int((k)//2)-1            
            if k>1:              
                if k%2:
                    x[k-1] =  x[P] + N/(2**Q)
                else:
                    x[k-1] =  x[P] - N/(2**Q)
                    
        Edges = np.vstack((np.repeat(np.arange(1,N),2),np.arange(2,2*N))).transpose() - 1
        labx = ["".join(k) for k in np.round(MSx,3).astype(str)]
        ax2 = subplot(G[3:,:])   
        ax2.scatter(x,y,s=100*(MSx-min(MSx)+1)/(abs(min(MSx))+1),color=(1,0,1))
        for k in range(len(x)-1):            
            ax2.plot(x[Edges[k,:]],y[Edges[k,:]],color=(8/255,63/255,77/255),linewidth=2.5)
            ax2.annotate(labx[k],(x[k],y[k]))  
        ax2.annotate(labx[-1],(x[-1],y[-1]))
        show()
    
    return MSx, Sn, CI


def Hierarchy(Z,sx):
    N = int(2**np.floor(np.log2(len(Z))))
    if np.log2(len(Z))%1 != 0:
        print('Only first %d samples were used in hierarchical decomposition. \
            \nThe last %d samples of the data sequence were ignored.'%(N,len(Z)-N))
    if N/(2**(sx-1)) < 8:
       raise Exception('Data length (%d) is too short to estimate entropy at the lowest' \
                      ' subtree. Consider reducing the number of scales.'%N) 
    
    U = np.zeros(((2**sx)-1,N))
    U[0,:] = Z[:N]
    p=1
    for k in range(sx-1):
        for n in range(2**k):
            Temp = U[(2**k)+n-1,:]        
            # U[p,1:N//2]  = (Temp[:-2:2] + Temp[1:-1:2])/2
            # U[p+1,1:N//2]= (Temp[:-2:2] - Temp[1:-1:2])/2
            U[p,:N//2]  = (Temp[::2] + Temp[1::2])/2
            U[p+1,:N//2]= (Temp[::2] - Temp[1::2])/2
            p+=2
    return U,N

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