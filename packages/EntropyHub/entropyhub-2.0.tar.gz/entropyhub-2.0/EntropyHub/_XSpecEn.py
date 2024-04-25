"""Base Cross Spectral Entropy function."""
import numpy as np  

def XSpecEn(*Sig, N=None, Freqs=(0,1), Logx=np.exp(1), Norm=True):
    """XSpecEn  estimates the cross-spectral entropy between two univariate data sequences.

    .. code-block:: python

        XSpec, BandEn = XSpecEn(Sig1, Sig2) 
        
    Returns the cross-spectral entropy estimate (``XSpec``) of the full cross-
    spectrum and the within-band entropy (``BandEn``) estimated for the data 
    sequences contained in ``Sig1`` and ``Sig2`` using the default  parameters: 
    N-point FFT = 2 * max length of ``Sig1``/``Sig2``, 
    normalised band edge frequencies = [0 1], logarithm = base 2, 
    normalisation = w.r.t # of spectrum/band frequency  values.
 
    .. code-block:: python
    
        XSpec, BandEn = XSpecEn(Sig1, Sig2, keyword = value, ...)
        
    Returns the cross-spectral entropy (``XSpec``) and the within-band entropy 
    (``BandEn``) estimate for the data sequences contained in ``Sig1`` and ``Sig2`` 
    using the  following specified 'keyword' arguments:
        :N:     - Resolution of spectrum (N-point FFT), an integer > 1
        :Freqs: - Normalised and edge frequencies, a scalar in range [0 1]  where 1 corresponds to the Nyquist frequency (Fs/2).
              * Note: When no band frequencies are entered, ``BandEn == SpecEn``
        :Logx:  - Logarithm base, a positive scalar     [default: natural]
        :Norm:  - Normalisation of ``XSpec`` value, one of the following integers:
            [false]  no normalisation.
            [true]   normalises w.r.t # of frequency values within the spectrum/band   [default]
    
    See the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_ for more info.
 
    
    :See also:
        ``SpecEn``, ``fft``, ``XDistEn``, ``periodogram``, ``XSampEn``, ``XApEn``
     
    :References:
        [1] Matthew W. Flood,
            "XSpecEn - EntropyHub Project"
            (2021) https://github.com/MattWillFlood/EntropyHub
    
    """


    assert len(Sig)<=2,  """Input arguments to be passed as data sequences:
        - A single Nx2 numpy matrix with each column representing Sig1 and Sig2 respectively.       \n or \n
        - Two individual numpy vectors representing Sig1 and Sig2 respectively."""
    if len(Sig)==1:
        Sig = np.squeeze(Sig)
        assert max(Sig.shape)>10 and min(Sig.shape)==2,  """Input arguments to be passed as data sequences:
            - A single Nx2 numpy matrix with each column representing Sig1 and Sig2 respectively.       \n or \n
            - Two individual numpy vectors representing Sig1 and Sig2 respectively."""
        if Sig.shape[0] == 2:
            Sig = Sig.transpose()  
        S1 = Sig[:,0]; S2 = Sig[:,1]     
        
    elif len(Sig)==2:
        S1 = np.squeeze(Sig[0])
        S2 = np.squeeze(Sig[1])
        
    if N is None:
        N = 2*max(len(S1),len(S2)) + 1
       
    assert min(len(S1),len(S2))>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"
    assert N>1 and isinstance(N,int), "N:   must be an integer > 1"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"       
    assert isinstance(Freqs,tuple) and len(Freqs)==2 and Freqs[0]>=0 and Freqs[1]<=1,\
            "Freq:    must be a two element tuple with values in range [0 1]. \
                      The values must be in increasing order."      
              
    Fx = int(np.ceil(N/2))
    Freqs = np.round(np.array(Freqs)*Fx).astype(int)-1
    Freqs[Freqs==-1] = 0
    
    if Freqs[0] > Freqs[1]:
        raise Exception('Lower band frequency must come first.')
    elif np.diff(Freqs) < 1:
        raise Exception('Spectrum resoution too low to determine bandwidth.')
    elif min(Freqs)<0 or max(Freqs)> Fx:
        raise Exception('Freqs must be normalized w.r.t sampling frequency [0 1].')  
        
    Pt = abs(np.fft.fft(np.convolve(S1,S2),N))
    Pxx = Pt[:Fx]/sum(Pt[:Fx])
    XSpec = -sum(Pxx*np.log(Pxx))/np.log(Logx)
    Pband = Pxx[Freqs[0]:Freqs[1]+1]/sum(Pxx[Freqs[0]:Freqs[1]+1])
    BandEn = -sum(Pband*np.log(Pband))/np.log(Logx)
    
    if Norm:
        XSpec = XSpec/(np.log(Fx)/np.log(Logx))
        BandEn = BandEn/(np.log(np.diff(Freqs)[0]+1)/np.log(Logx))
    return XSpec, BandEn

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