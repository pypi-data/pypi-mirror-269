"""Base Phase Entropy function."""
import numpy as np
import matplotlib.pyplot as mpl

def PhasEn(Sig, K=4, tau=1, Logx=np.exp(1), Norm=True, Plotx=False):
    """PhasEn  estimates the phase entropy of a univariate data sequence.

    .. code-block:: python
    
        Phas = PhasEn(Sig) 
        
    Returns the phase entropy (``Phas``) estimate of the data sequence (``Sig``)
    using the default parameters: angular partitions = 4, time delay = 1, logarithm = natural,
 
    .. code-block:: python
    
        Phas = PhasEn(Sig, keyword = value, ...)
        
    Returns the phase entropy (``Phas``) estimate of the data sequence (``Sig``)  
    using the specified 'keyword' arguments:
        :K:     - Angular partitions (coarse graining), an integer > 1
                  Note: Division of partitions begins along the positive
                        x-axis. As this point is somewhat arbitrary, it is
                        recommended to use even-numbered (preferably
                        multiples of 4) partitions for sake of symmetry. 
        :tau:   - Time Delay, a positive integer
        :Logx:  - Logarithm base, a positive scalar  
        :Norm:  - Normalisation of Phas value, a boolean:
            - [false]  no normalisation
            - [true]   normalises w.r.t. the # partitions ``Log(K)``  (Default)
            
    :Plotx: - When ``Plotx == true``, returns second-order difference plot (default: false)
    
    :See also:
        ``SampEn``, ``ApEn``, ``GridEn``, ``MSEn``, ``SlopEn``, ``CoSiEn``, ``BubbEn``
    
    :References:
        [1] Ashish Rohila and Ambalika Sharma,
            "Phase entropy: a new complexity measure for heart rate
            variability." 
            Physiological measurement
            40.10 (2019): 105006.
    
    """
    
    Sig = np.squeeze(Sig)
   
    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert isinstance(K,int) and (K > 1), "K:     must be an integer > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(Logx,(int,float)) and Logx>0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"  
    assert isinstance(Plotx,bool), "Plotx:     must be boolean - True or False"                          
        
    Yn = Sig[2*tau:] - Sig[tau:-tau]
    Xn = Sig[tau:-tau] - Sig[:-2*tau]    
    with np.errstate(divide='ignore', invalid='ignore'):
        Theta_r = np.arctan(Yn/Xn)   
        Theta_r[np.logical_and((Yn<0),(Xn<0))] += np.pi
        Theta_r[np.logical_and((Yn<0),(Xn>0))] += 2*np.pi
        Theta_r[np.logical_and((Yn>0),(Xn<0))] += np.pi
    
    Limx = np.ceil(np.max(np.abs([Yn, Xn])))
    Angs = np.linspace(0,2*np.pi,K+1)
    Tx = np.zeros((K,len(Theta_r)))
    Si = np.zeros(K)
    
    for n in range(K):
        Temp = np.logical_and((Theta_r > Angs[n]), (Theta_r < Angs[n+1]))
        Tx[n,Temp] = 1
        Si[n] = np.sum(Theta_r[Temp])
            
    Si = Si[Si!=0]
    Phas = -np.sum((Si/np.sum(Si))*(np.log(Si/np.sum(Si))/np.log(Logx)))
    if Norm:
        Phas = Phas/(np.log(K)/np.log(Logx))
    
    if Plotx:

        Tx = Tx.astype(bool)
        Ys = np.sin(Angs)*Limx*np.sqrt(2)
        Xs = np.cos(Angs)*Limx*np.sqrt(2)
        Cols = np.transpose(np.vstack((np.zeros(K), np.tile((np.random.permutation(K)+1)/K,(2,1)))))
        mpl.figure()
        for n in range(K):
            mpl.plot(Xn[Tx[n,:]],Yn[Tx[n,:]],'.',color=tuple(Cols[n,:]))
            mpl.plot(np.vstack((np.zeros(K+1),Xs)),np.vstack((np.zeros(K+1),Ys)),color='m')
        mpl.axis([-Limx, Limx, -Limx, Limx])
        mpl.gca().set_aspect('equal','box')
        mpl.xlabel(r'$X(n +  \tau)  -  X(n)$'), 
        mpl.ylabel(r'$X(n + 2 \tau)  -  X(n + \tau)$')
        mpl.xticks([-Limx, 0, Limx])
        mpl.yticks([-Limx, 0, Limx])
        mpl.show()
    
    return Phas
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