

from EntropyHub._ApEn import ApEn
from EntropyHub._AttnEn import AttnEn
from EntropyHub._BubbEn import BubbEn
from EntropyHub._CondEn import CondEn
from EntropyHub._CoSiEn import CoSiEn
from EntropyHub._DistEn import DistEn
from EntropyHub._DispEn import DispEn
from EntropyHub._DivEn import DivEn
from EntropyHub._EnofEn import EnofEn
from EntropyHub._FuzzEn import FuzzEn
from EntropyHub._GridEn import GridEn
from EntropyHub._IncrEn import IncrEn
from EntropyHub._K2En import K2En
from EntropyHub._PhasEn import PhasEn
from EntropyHub._PermEn import PermEn
from EntropyHub._RangEn import RangEn
from EntropyHub._SampEn import SampEn
from EntropyHub._SpecEn import SpecEn
from EntropyHub._SlopEn import SlopEn
from EntropyHub._SyDyEn import SyDyEn


from EntropyHub._XApEn import XApEn
from EntropyHub._XCondEn import XCondEn 
from EntropyHub._XDistEn import XDistEn 
from EntropyHub._XFuzzEn import XFuzzEn
from EntropyHub._XK2En import XK2En
from EntropyHub._XPermEn import XPermEn
from EntropyHub._XSampEn import XSampEn
from EntropyHub._XSpecEn import XSpecEn


from EntropyHub._SampEn2D import SampEn2D
from EntropyHub._FuzzEn2D import FuzzEn2D
from EntropyHub._DistEn2D import DistEn2D
from EntropyHub._DispEn2D import DispEn2D
from EntropyHub._EspEn2D import EspEn2D
from EntropyHub._PermEn2D import PermEn2D


from EntropyHub._MvSampEn import MvSampEn
from EntropyHub._MvFuzzEn import MvFuzzEn
from EntropyHub._MvCoSiEn import MvCoSiEn
from EntropyHub._MvDispEn import MvDispEn
from EntropyHub._MvPermEn import MvPermEn


from EntropyHub._ExampleData import ExampleData
from EntropyHub._WindowData import WindowData
from EntropyHub._MSobject import MSobject


from EntropyHub._MSEn import MSEn
from EntropyHub._cMSEn import cMSEn
from EntropyHub._rMSEn import rMSEn
from EntropyHub._hMSEn import hMSEn

from EntropyHub._XMSEn import XMSEn
from EntropyHub._cXMSEn import cXMSEn
from EntropyHub._rXMSEn import rXMSEn
from EntropyHub._hXMSEn import hXMSEn

from EntropyHub._MvMSEn import MvMSEn
from EntropyHub._cMvMSEn import cMvMSEn

# from EntropyHub._MSEn2D import MSEn2D


def greet():
    print("""
    
    	 ___  _   _  _____  _____  ____  ____  _     _          
    	|  _|| \ | ||_   _||     \|    ||    || \   / |   ___________ 
    	| \_ |  \| |  | |  |   __/|    ||  __| \ \_/ /   /  _______  \\
    	|  _|| \ \ |  | |  |   \  |    || |     \   /   |  /  ___  \  |
    	| \_ | |\  |  | |  | |\ \ |    || |      | |    | |  /   \  | | 
    	|___||_| \_|  |_|  |_| \_||____||_|      |_|   _|_|__\___/  | | 
    	 _   _  _   _  ____                           / |__\______\/  | 
    	| | | || | | ||    \     An open-source      |  /\______\__|_/ 
    	| |_| || | | ||    |     toolkit for         | |  /   \  | | 
    	|  _  || | | ||    \     entropic time-      | |  \___/  | |          
    	| | | || |_| ||     \    series analysis     |  \_______/  |
    	|_| |_|\_____/|_____/                         \___________/ 
    
          
        Please use the following citation on any scientific outputs achieved with the help of EntropyHub:
        
        Matthew W. Flood,
        EntropyHub: An Open-Source Toolkit for Entropic Time Series Analysis,
        PLoS One 16(11):e0259448 (2021),
        DOI: 10.1371/journal.pone.0259448

        www.EntropyHub.xyz
        
        """)
    
def functionlist():
    print("""    
        EntropyHub functions belong to one of five main classes/categories:
        Base Entropies             >>  e.g. Approximate Entropy (ApEn),
                                            Sample Entropy (SampEn)
        Cross Entropies            >>  e.g. Cross-Approximate Entropy (XApEn)
                                            Cross-Sample Entropy (XSampEn)
        Bidimensional Entropies    >>  e.g. Bidimensional Sample Entropy (SampEn2D)
                                            Bidimensional Fuzzy Entropy (FuzzEn2D)
        Multiscale Entropies       >>  e.g. Multiscale Sample Entropy (MSEn)
                                            Refined Multiscale Sample Entropy (rMSEn)
                                            Composite Multiscale Sample Entropy (cMSEn)
        Multiscale Cross Entropies >>  e.g. Multiscale Cross-Sample Entropy (XMSEn)
                                            Refined Multiscale Cross-Sample Entropy (rXMSEn)
        
        _________________________________________________________________________
        Base Entropies                                     	|	Function Name
        ____________________________________________________|__________________
        Approximate Entropy                               	|	ApEn
        Sample Entropy                                    	|	SampEn
        Fuzzy Entropy                                     	|	FuzzEn
        Kolmogorov Entropy                                	|	K2En
        Permutation Entropy                               	|	PermEn
        Conditional Entropy                               	|	CondEn
        Distribution Entropy                              	|	DistEn
        Spectral Entropy                                  	|	SpecEn
        Dispersion Entropy                                	|	DispEn
        Symbolic Dynamic Entropy                          	|	SyDyEn
        Increment Entropy                                 	|	IncrEn
        Cosine Similarity Entropy                         	|	CoSiEn
        Phase Entropy                                      	|	PhasEn
        Slope Entropy                                      	|	SlopEn
        Bubble Entropy                                      |	BubbEn
        Gridded Distribution Entropy                        |	GridEn
        Entropy of Entropy                                  |	EnofEn
        Attention Entropy                                   |	AttnEn
        Diversity Entropy                                   |	DivEn
        Range Entropy                                       |	RangEn
        
        _______________________________________________________________________
        Cross Entropies                                     |	Function Name
        ____________________________________________________|__________________
        Cross Sample Entropy                                |	XSampEn
        Cross Approximate Entropy                           |	XApEn
        Cross Fuzzy Entropy                                 |	XFuzzEn
        Cross Permutation Entropy                           |	XPermEn
        Cross Conditional Entropy                           |	XCondEn
        Cross Distribution Entropy                          |	XDistEn
        Cross Spectral Entropy                              |	XSpecEn
        Cross Kolmogorov Entropy                           	|	XK2En
        	
        _________________________________________________________________________
        Bidimensional Entropies                              |	Function Name
        _____________________________________________________|___________________
        Bidimensional Sample Entropy                         |	SampEn2D
        Bidimensional Fuzzy Entropy                          |	FuzzEn2D
        Bidimensional Distribution Entropy                   |	DistEn2D
        Bidimensional Dispersion Entropy                     |	DispEn2D
        Bidimensional Permutation Entropy                    |	PermEn2D
        Bidimensional Espinosa Entropy                       |	EspEn2D
        
        _________________________________________________________________________
        Multivariate Entropies                               |	Function Name
        _____________________________________________________|___________________
        Multivariate Sample Entropy                          |	MvSampEn
        Multivariate Fuzzy Entropy                           |	MvFuzzEn
        Multivariate Cosine Similarity Entropy               |	MvCoSiEn
        Multivariate Dispersion Entropy                      |	MvDispEn
        Multivariate Permutation Entropy                     |	MvPermEn
        	
        _________________________________________________________________________
        Multiscale Entropy Functions                          | Function Name
        ______________________________________________________|__________________ 
        Multiscale Entropy Object                             |   MSobject
                                                              |
        Multiscale Entropy                                    |   MSEn
        Composite/Refined-Composite Multiscale Entropy        |   cMSEn
        Refined Multiscale Entropy                            |   rMSEn
        Hierarchical Multiscale Entropy Object                |   hMSEn
        
        _________________________________________________________________________
        Multiscale Entropies	MSEn                          |	Function Name
        ______________________________________________________|__________________
        Multiscale Sample Entropy                             |	
        Multiscale Approximate Entropy                        |	
        Multiscale Fuzzy Entropy                              |	
        Multiscale Permutation Entropy                        |	
        Multiscale Dispersion Entropy                         |	
        Multiscale Cosine Similarity Entropy                  |	
        Multiscale Symblic Dynamic Entropy                    |	MSobject
        Multiscale Conditional Entropy                        |	     +
        Multiscale Entropy of Entropy                         |   MSEn / cMSEn
        Multiscale Gridded Distribution Entropy               |	rMSEn / hMSEn
        Multiscale Slope Entropy                              |
        Multiscale Phase Entropy                              |		
        Multiscale Kolmogorov Entropy                         |	
        Multiscale Distribution Entropy                       |	
        Multiscale Bubble Entropy                             |	
        Multiscale Increment Entropy                          |	
        Multiscale Attention Entropy                          |	
        Multiscale Diversity Entropy                          |	
        Multiscale Range Entropy                              |	
        	
        _________________________________________________________________________
        Multiscale Cross-Entropy Functions                    |   Function Name
        ______________________________________________________|__________________
        Multiscale Cross-Entropy Object                       |   MSobject
                                                              |
        Multiscale Cross-Entropy                              |   XMSEn
        Composite/Refined-Composite Multiscale Cross-Entropy  |   cXMSEn
        Refined Multiscale Entropy                            |   rXMSEn
        Hierarchical Multiscale Entropy Object                |   hXMSEn
        
        _________________________________________________________________________
        Multiscale Cross-Entropies                            |	Function Name
        ______________________________________________________|__________________
        Multiscale Cross-Sample Entropy                       |	
        Multiscale Cross-Approximate Entropy                  |	
        Multiscale Cross-Fuzzy Entropy                        |	MSobject
        Multiscale Cross-Permutation Entropy                  |	    +
        Multiscale Cross-Distribution Entropy                 |	XMSEn / cXMSEn
        Multiscale Cross-Kolmogorov Entropy                   |   rXMSEn / hXMSEn
        Multiscale Cross-Conditional Entropy                  |	
        
        _________________________________________________________________________
        Multivariate Multiscale Entropies                     |	Function Name
        ______________________________________________________|__________________
        Multivariate Multiscale Sample Entropy                |	
        Multivariate Multiscale Fuzzy Entropy                 |	MSobject
        Multivariate Multiscale Dispersion Entropy            |	    +
        Multivariate Multiscale Permutation Entropy           |	MvMSEn / cMvMSEn
        Multivariate Multiscale Cosine Similarity Entropy     |	
        
        
        
        This package is open for use by all in accordance with the terms of the 
        attached License agreement. Any scientific outputs obtained using 
        EntropyHub are required to include the following citation:
        
          Matthew W. Flood, 
          "EntropyHub: An open-source toolkit for entropic time series analysis",
          2021, https://github.com/MattWillFlood/EntropyHub
        
          © Copyright 2024 Matthew W. Flood, EntropyHub
        
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
        
        """)


        # _________________________________________________________________________
        # Multiscale Bidimensional Entropy Functions            |   Function Name
        # ______________________________________________________|__________________
        # Multiscale Bidimensional Entropy Object               |   MSobject
        #                                                       |
        # Multiscale Bidimensional Entropy                      |   MSEn2D
        
        # _________________________________________________________________________
        # Multiscale Bidimensional-Entropies                    |	Function Name
        # ______________________________________________________|__________________
        # Multiscale Bidimensional Sample Entropy               |	
        # Multiscale Bidimensional Fuzzy Entropy                |	
        # Multiscale Bidimensional Distribution Entropy         |	MSobject
        # Multiscale Bidimensional Dispersion Entropy           |	    +
        # Multiscale Bidimensional Permutation Entropy          |	 MSEn2D
        # Multiscale Bidimensional Espinosa Entropy             |
