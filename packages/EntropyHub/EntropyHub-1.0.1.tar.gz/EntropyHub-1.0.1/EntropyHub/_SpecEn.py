"""Base Spectral Entropy function."""
import numpy as np  

def SpecEn(Sig, N=None, Freqs=(0,1), Logx=np.exp(1), Norm=True):
    """SpecEn  estimates the spectral entropy of a univariate data sequence.

    .. code-block:: python
    
        Spec, BandEn = SpecEn(Sig) 
    
    Returns the spectral entropy estimate of the full spectrum (``Spec``)
    and the within-band entropy (BandEn) estimated from the data sequence (``Sig``)
    using the default  parameters: 
    N-point FFT = 2*len(Sig) + 1, normalised band edge frequencies = [0 1],
    logarithm = base 2, normalisation = w.r.t # of spectrum/band frequency values.
 
    .. code-block:: python
    
        Spec, BandEn = SpecEn(Sig, keyword = value, ...)
        
    Returns the spectral entropy (``Spec``) and the within-band entropy (``BandEn``)
    estimate from the data sequence (``Sig``) using the specified 'keyword' arguments:
        :N:     - Resolution of spectrum (N-point FFT), an integer > 1
        :Freqs: - Normalised band edge frequencies, a 2 element tuple with values in range [0 1] where 1 corresponds to the Nyquist frequency (Fs/2).
             * Note: When no band frequencies are entered, ``BandEn == SpecEn``
        :Logx:  - Logarithm base, a positive scalar (enter 0 for natural log) 
        :Norm:  - Normalisation of Spec value, a boolean:
           * [False]  no normalisation.
           * [True]   normalises w.r.t # of spectrum/band frequency values - default.
 
    For more info, see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``XSpecEn``, ``MSEn``, ``numpy.fftpack``
          
    :References:
        [1] G.E. Powell and I.C. Percival,
            "A spectral entropy method for distinguishing regular and 
            irregular motion of Hamiltonian systems." 
            Journal of Physics A: Mathematical and General 
            12.11 (1979): 2053.
    
        [2] Tsuyoshi Inouye, et al.,
            "Quantification of EEG irregularity by use of the entropy of 
            the power spectrum." 
            Electroencephalography and clinical neurophysiology 
            79.3 (1991): 204-210.
    
    """
  
    Sig = np.squeeze(Sig)            
    if N is None:
        N = 2*len(np.squeeze(Sig)) + 1
    
    assert Sig.shape[0]>10 and Sig.ndim == 1,  "Sig:   must be a numpy vector"
    assert N>1 and isinstance(N,int), "N:   must be an integer > 1"
    assert isinstance(Logx,(int,float)) and Logx > 0, "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be boolean - True or False"       
    assert isinstance(Freqs,tuple) and len(Freqs)==2 and Freqs[0]>=0 and Freqs[1]<=1,\
            "Freq:    must be a two element tuple with values in range [0 1]. \
                      The values must be in increasing order."  
        
    Fx = int(np.ceil(N/2))
    Freqs = np.round(np.array(Freqs)*Fx).astype(int)-1
    Freqs[Freqs==-1] = 0    
    if Freqs[0] > Freqs[1]:
        raise Exception('Lower band frequency must come first.')
    elif Freqs[1] - Freqs[0] < 1:
        raise Exception('Spectrum resoution too low to determine bandwidth.') 
    elif min(Freqs)<0 or max(Freqs)>Fx:
        raise Exception('Freqs must be normalized w.r.t. sampling frequency [0 1].')
        
    Pt = abs(np.fft.fft(np.convolve(Sig,Sig),N))
    Pxx = Pt[:Fx]/sum(Pt[:Fx])
    Spec = -sum(Pxx*np.log(Pxx))/np.log(Logx)
    Pband = Pxx[Freqs[0]:Freqs[1]+1]/sum(Pxx[Freqs[0]:Freqs[1]+1])
    BandEn = -sum(Pband*np.log(Pband))/np.log(Logx)
    
    if Norm:
        Spec = Spec/(np.log(Fx)/np.log(Logx))
        BandEn = BandEn/(np.log(np.diff(Freqs)[0]+1)/np.log(Logx))
    return Spec, BandEn
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