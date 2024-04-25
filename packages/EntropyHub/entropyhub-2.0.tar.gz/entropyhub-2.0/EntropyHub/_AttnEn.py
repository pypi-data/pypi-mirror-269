""" Attention Entropy function."""
import numpy as np

def AttnEn(Sig, Logx=2):
    """AttnEn  estimates the attention entropy of a univariate data sequence.
    
    .. code-block:: python
    
        Attn, (Hxx, Hnn, Hxn, Hnx) = AttnEn(Sig)
    
    Returns the attention entropy (``Attn``) calculated as the average of the
    sub-entropies (``Hxx``, ``Hxn``, ``Hnn``, ``Hnx``) estimated from the data sequence (``Sig``) 
    using a base-2 logarithm.
    
    .. code-block:: python
    
        Attn, (Hxx, Hnn, Hxn, Hnx) = AttnEn(Sig, Logx = value)
    
    Returns the attention entropy (``Attn``) and a four-element tuple of
    sub-entropies (``Hxx``, ``Hnn``, ``Hxn``, ``Hnx``) from the data sequence (``Sig``) where,
        :Hxx:  -  entropy of local-maxima intervals
        :Hnn: -   entropy of local minima intervals
        :Hxn: -   entropy of intervals between local maxima and subsequent minima
        :Hnx:   - entropy of intervals between local minima and subsequent maxima using the following keyword argument:
        :Logx:  - Logarithm base, a positive scalar  (enter 0 for natural log)
    
    :See also:
        ``EnofEn``, ``SpecEn``, ``XSpecEn``, ``PermEn``, ``MSEn``
    
    :References:
        [1] Jiawei Yang, et al.,
            "Classification of Interbeat Interval Time-series Using Attention Entropy." 
            IEEE Transactions on Affective Computing 
            (2020)
    """

    Sig = np.squeeze(Sig)
    N = Sig.shape[0]
    if Logx == 0:
        Logx = np.exp(1) 
    assert N>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"

    Xmax = PkFind(Sig)
    Xmin = PkFind(-Sig)
    Txx = np.diff(Xmax)
    Tnn = np.diff(Xmin)
    Temp = np.diff(np.sort(np.hstack((Xmax, Xmin))))
    
    assert len(Xmax) > 0, "No local maxima found!"
    assert len(Xmin) > 0, "No local minima found!" 
    
    if Xmax[0]<Xmin[0]:
       Txn = Temp[::2]
       Tnx = Temp[1::2]
    else:
       Txn = Temp[1::2]
       Tnx = Temp[::2]
       
    Edges = np.arange(-0.5,N+1)
    Pnx,_ = np.histogram(Tnx,Edges)
    Pnn,_ = np.histogram(Tnn,Edges)
    Pxx,_ = np.histogram(Txx,Edges)
    Pxn,_ = np.histogram(Txn,Edges)
    
    Pnx = Pnx[Pnx!=0]/len(Tnx)
    Pxn = Pxn[Pxn!=0]/len(Txn)
    Pnn = Pnn[Pnn!=0]/len(Tnn)
    Pxx = Pxx[Pxx!=0]/len(Txx)
    
    Hxx = -sum(Pxx*np.log(Pxx)/np.log(Logx))
    Hxn = -sum(Pxn*np.log(Pxn)/np.log(Logx))
    Hnx = -sum(Pnx*np.log(Pnx)/np.log(Logx))
    Hnn = -sum(Pnn*np.log(Pnn)/np.log(Logx))
    Av4 = (Hnn + Hxx + Hxn + Hnx)/4
    
    return Av4, (Hxx,Hnn,Hxn,Hnx)


def PkFind(X):
    Nx = len(X)
    Indx = np.zeros(Nx)
    for n in range(1,Nx-1):
        if X[n-1] < X[n] > X[n+1]:
            Indx[n] = n

        elif X[n-1] < X[n] == X[n+1]:
            k = 1
            while (n+k)<Nx-1 and X[n] == X[n+k]:
                k += 1
            
            if X[n] > X[n+k]:
                Indx[n] = n + ((k-1)//2)

    Indx = Indx[Indx!=0]
    return Indx

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