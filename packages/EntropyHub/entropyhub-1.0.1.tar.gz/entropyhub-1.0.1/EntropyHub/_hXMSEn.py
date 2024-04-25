"Base hierarchical cross-Multiscale Entropy function."
import numpy as np
from matplotlib.pyplot import figure, show, subplot
import matplotlib.gridspec as gridspec
from copy import deepcopy

def hXMSEn(Sig1, Sig2, Mbjx, Scales=3, RadNew=0, Plotx=False):
    """hXMSEn  returns the hierarchical cross-entropy between two univariate data sequences.

    .. code-block:: python
    
        MSx, Sn, CI = hXMSEn(Sig1, Sig2, Mobj) 
        
    Returns a vector of cross-entropy values (``MSx``) calculated at each node 
    in the hierarchical tree, the average cross-entropy value across all 
    nodes at each scale (``Sn``), and the complexity index (``CI``) of the hierarchical 
    tree (i.e. ``sum(Sn)``) between the data sequences contained in ``Sig1`` and``Sig2`` using
    the parameters specified by the multiscale object (``Mobj``) over 3 temporal scales (default).
    The entropy values in ``MSx`` are ordered from the root node (S_00) to the
    Nth subnode at scale T (S_TN): i.e. S_00, S_10, S_11, S_20, S_21, S_22,
    S_23, S_30, S_31, S_32, S_33, S_34, S_35, S_36, S_37, S_40, ... , S_TN.
    The average cross-entropy values in Sn are ordered in the same way, with the
    value of the root node given first: i.e. S0, S1, S2, ..., ST
     
    .. code-block:: python
    
        MSx, Sn, CI = hXMSEn(Sig1, Sig2, Mobj, Keyword = value, ...)
        
    Returns a vector of cross-entropy values (``MSx``) calculated at each node 
    in the hierarchical tree, the average cross-entropy value across all
    nodes at each scale (``Sn``), and the complexity index (``CI``) of the entire
    hierarchical tree between the data sequences contained in ``Sig1`` and ``Sig2`` using 
    the following keyword arguments:
        :Scales:   - Number of temporal scales, an integer > 1   (default: 3)
        :RadNew:   - Radius rescaling method, an integer in the range [1 4].
                     When the cross-entropy specified by ``Mobj`` is ``XSampEn`` or ``XApEn``, RadNew rescales the radius threshold in each sub-sequence
                     at each time scale (Ykj). If a radius value (``r``) is specified by ``Mobj``, this becomes the rescaling coefficient, otherwise
                     it is set to 0.2 (default). The value of RadNew specifies one of the following methods:
                    
                        * [1] Pooled Standard Deviation   - ``r*std(Ykj)``
                        * [2] Pooled Variance             - ``r*var(Ykj)``
                        * [3] Mean Absolute Deviation     - ``r*mad(Ykj)``
                        * [4] Median Absolute Deviation   - ``r*mad(Ykj,1)``
                        
        :Plotx:    - When ``Plotx == True``, returns a plot of the average cross-entropy value at each time scale (i.e. the multiscale cross-entropy curve) and a hierarchical graph showing the cross-entropy value of each node in the hierarchical tree decomposition.  (default: False)
    
    :See also:
        ``MSobject``, ``XMSEn``, ``rXMSEn``, ``cXMSEn``, ``XSampEn``, ``XApEn``, ``MSEn``, ``hMSEn``, ``rMSEn``, ``cMSEn``
    
    :References:
        [1]   Matthew W. Flood,
            "hXMSEn - EntropyHub Project"
            2021, https://github.com/MattWillFlood/EntropyHub
        [2]   Rui Yan, Zhuo Yang, and Tao Zhang,
            "Multiscale cross entropy: a novel algorithm for analyzing two
            time series." 
            5th International Conference on Natural Computation. 
            Vol. 1, pp: 411-413 IEEE, 2009.
    
        [3] Ying Jiang, C-K. Peng and Yuesheng Xu,
            "Hierarchical entropy analysis for biological signals."
            Journal of Computational and Applied Mathematics
            236.5 (2011): 728-742.
    
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
    assert (np.isin(RadNew,np.arange(1,5)) and Mobj.Func.__name__ in \
    ['XSampEn','XApEn']) or RadNew==0, "RadNew:     must be an integer in range \
    [1 4] and entropy function must be 'XSampEn' or 'XApEn'"
    assert isinstance(Plotx, bool), "Plotx:    must be boolean - True or False"
              
    if Mobj.Func.__name__ in 'XSampEn': Mobj.Kwargs['Vcp'] = False 
    
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
        
    XX, YY, N1, N2 = Hierarchy(S1,S2,Scales)
    MSx = np.zeros(XX.shape[0])
    for T in range(XX.shape[0]):
        print(' .', end='')
        
        Xa = XX[T,:int(N1/(2**(int(np.log2(T+1)))))]
        Xb = YY[T,:int(N2/(2**(int(np.log2(T+1)))))]

        if RadNew:
            Mobj.Kwargs.update({'r': Cx*Rnew(Xa,Xb)})            
        Temp2 = Mobj.Func(Xa,Xb,**Mobj.Kwargs)
        
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
       
    CI = sum(Sn)
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

    
def Hierarchy(Za, Zb, sx):
    Na = int(2**np.floor(np.log2(len(Za))))
    if np.log2(len(Za))%1 != 0:
        print('WARNING: Only first %d samples were used in hierarchical decomposition. \
            \nThe last %d samples of the data sequence were ignored.'%(Na,len(Za)-Na))
    if Na/(2**(sx-1)) < 8:
       raise Exception('Data length (%d) is too short to estimate entropy at the lowest' \
                      ' subtree. Consider reducing the number of scales.'%Na) 
                      
    Nb = int(2**np.floor(np.log2(len(Zb))))
    if np.log2(len(Zb))%1 != 0:
        print('WARNING: Only first %d samples were used in hierarchical decomposition. \
            \nThe last %d samples of the data sequence were ignored.'%(Nb,len(Zb)-Nb))
    if Nb/(2**(sx-1)) < 8:
       raise Exception('Data length (%d) is too short to estimate entropy at the lowest' \
                      ' subtree. Consider reducing the number of scales.'%Nb) 
    
    Za = Za[:Na]
    Zb = Zb[:Nb]
    
    U1 = np.zeros(((2**sx)-1,Na))
    U1[0,:] = Za
    p=1
    for k in range(sx-1):
        for n in range(2**k):
            Temp = U1[(2**k)+n-1,:]        
            U1[p,:Na//2]  = (Temp[::2] + Temp[1::2])/2
            U1[p+1,:Na//2]= (Temp[::2] - Temp[1::2])/2            
            p+=2
            
    U2 = np.zeros(((2**sx)-1,Nb))
    U2[0,:] = Zb
    p=1
    for k in range(sx-1):
        for n in range(2**k):
            Temp = U2[(2**k)+n-1,:]        
            U2[p,:Nb//2]  = (Temp[::2] + Temp[1::2])/2
            U2[p+1,:Nb//2]= (Temp[::2] - Temp[1::2])/2
            p+=2
                            
    return U1, U2, Na, Nb

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