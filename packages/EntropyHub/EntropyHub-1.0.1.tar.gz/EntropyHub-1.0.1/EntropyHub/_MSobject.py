"""Base MSobject function."""

def MSobject(EnType='SampEn', **kwargs):
    """MSobject  creates an object to store multiscale entropy parameters.
    
    .. code-block:: python
    
        [Mobj] = MSobject() 
        
    Returns a multiscale entropy object (``Mobj``) based on that originally
    proposed by Costa et al. using the following default  parameters:
    EnType = 'SampEn', embedding dimension = 2, time delay = 1, 
    radius = 0.2*SD(``Sig``), logarithm = natural
     
    .. code-block:: python
    
        [Mobj] = MSobject(EnType)
        
    Returns a multiscale entropy object using the specified entropy method
    (``EnType``) and the default parameters for that entropy method.
    To see the default parameters for a particular entropy method,          
    type:   `help(EnType)`   (e.g.  ``help(SampEn)``)
    
    .. code-block:: python
    
        [Mobj] = MSobject(EnType, keyword = value, ...)
        
    Returns a multiscale entropy object using the specified entropy method
    (``EnType``) and the name/value parameters for that particular method.
    To see the default parameters for a particular entropy method,          
    type:   `help(EnType)`   (e.g.  ``help(SampEn)``)
    
    ``EnType`` can be any of the following (case sensitive) string names:
    
    :Base Entropies: 
        :``'ApEn'``:      - Approximate Entropy
        :``'SampEn'``:    - Sample Entropy
        :``'FuzzEn'``:    - Fuzzy Entropy
        :``'K2En'``:      - Kolmogorov Entropy
        :``'PermEn'``:    - Permutation Entropy	
        :``'CondEn'``:    - Conditional Entropy	
        :``'DistEn'``:    - Distribution Entropy	
        :``'DispEn'``:    - Dispersion Entropy	
        :``'SpecEn'``:    - Spectral Entropy
        :``'SyDyEn'``:    - Symbolic Dynamic Entropy	
        :``'IncrEn'``:    - Increment Entropy	
        :``'CoSiEn'``:    - Cosine Similarity Entropy	
        :``'PhasEn'``:    - Phase Entropy	
        :``'SlopEn'``:    - Slope Entropy
        :``'BubbEn'``:    - Bubble Entropy	
        :``'GridEn'``:    - Grid Distribution Entropy	
        :``'EnofEn'``:    - Entropy of Entropy	
        :``'AttnEn'``:    - Attention Entropy
        [``'DivEn'``]:    - Diversity Entropy
        [``'RangEn'``]:   - Range Entropy
        
    
    :Cross Entropies:    
        :``'XApEn'``:     - Cross-Approximate Entropy
        :``'XSampEn'``:   - Cross-Sample Entropy
        :``'XFuzzEn'``:   - Cross-Fuzzy Entropy
        :``'XK2En'``:     - Cross-Kolmogorov Entropy
        :``'XPermEn'``:   - Cross-Permutation Entropy
        :``'XCondEn'``:   - Cross-Conditional Entropy (corrected)
        :``'XDistEn'``:   - Cross-Distribution Entropy
        :``'XSpecEn'``:   - Cross-Spectral Entropy
        
     
    :Multivariate Entropies:          
        :``'MvSampEn'``:   - Multivariate Sample Entropy
        :``'MvFuzzEn'``:   - Multivariate Fuzzy Entropy
        :``'MvDispEn'``:   - Multivariate Dispersion Entropy
        :``'MvCoSiEn'``:   - Multivariate Cosine Similarity Entropy
        :``'MvPermEn'``:   - Multivariate Permutation Entropy   

    
    :See also:
        ``MSEn``, ``cMSEn``, ``rMSEn``, ``hMSEn``, ``XMSEn``, ``rXMSEn``, ``cXMSEn``, ``hXMSEn``    
    """
        
    Chk = ['_ApEn',   '_SampEn', '_FuzzEn', '_K2En',   '_PermEn', '_CondEn', 
           '_DistEn', '_DispEn', '_SyDyEn', '_IncrEn', '_CoSiEn', '_PhasEn', 
           '_SpecEn', '_SlopEn', '_GridEn', '_BubbEn', '_EnofEn', '_AttnEn',
           '_DivEn', '_RangEn', 
           '_XApEn', '_XSampEn', '_XFuzzEn', '_XPermEn', 
           '_XCondEn', '_XDistEn','_XSpecEn', '_XK2En', 
           '_MvSampEn', '_MvFuzzEn', '_MvDispEn', '_MvPermEn','_MvCoSiEn']
    
    assert ('_'+EnType) in Chk, "EnType:      must be a valid entropy function name. \
    See help(EntropyHub.MSobject) for more info."
                
    class MS_Entropy:
        def __init__(self, EnType, X):
            # _temp = __import__(('_'+EnType), globals(), locals(), [EnType], 0)
            
            #_temp = __import__(('EntropyHub._'+EnType), fromlist=[EnType])
            _temp = __import__('_'+EnType)
            
            self.Func = getattr(_temp,EnType) 
            self.Kwargs = X
    
    Mobj = MS_Entropy(EnType, kwargs)   
    return Mobj

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