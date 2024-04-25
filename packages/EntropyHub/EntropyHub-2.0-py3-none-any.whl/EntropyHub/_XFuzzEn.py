"""Base Cross Fuzzy Entropy function."""
import numpy as np
    
def XFuzzEn(*Sig, m=2, tau=1, r=(.2,2.0), Fx= 'default', Logx=np.exp(1)):
    """XFuzzEn  estimates the cross-fuzzy entropy between two univariate data sequences.

    .. code-block:: python
    
        XFuzz, Ps1, Ps2 = XFuzzEn(Sig1,Sig2) 
    
    Returns the cross-fuzzy entropy estimates (``XFuzz``) and the average fuzzy
    distances (``m: Ps1``, ``m+1: Ps2``) for ``m`` = [1,2] estimated for the data sequences
    contained in ``Sig1`` and ``Sig2``, using the default parameters: embedding dimension = 2,
    time delay = 1, fuzzy function (``Fx``) = 'default', 
    fuzzy function parameters (``r``) = (0.2, 2), logarithm = natural
    
    .. code-block:: python
    
        XFuzz, Ps1, Ps2 = XFuzzEn(Sig1, Sig2, keyword = value, ...)
        
    Returns the cross-fuzzy entropy estimates (``XFuzz``) for dimensions = [1, ..., ``m``]
    estimated for the data sequences in ``Sig1`` and ``Sig2`` using the specified 'keyword' arguments:
        :m:     - Embedding Dimension, a positive integer   [default: 2]
        :tau:   - Time Delay, a positive integer            [default: 1]
        :Fx:    - Fuzzy function name, one of the following strings:  
            {``'sigmoid'``, ``'modsampen'``, ``'default'``, ``'gudermannian'``, ``'bell'``, ``'triangular'``, ``'trapezoidal1'``, ``'trapezoidal2'``, ``'z_shaped'``, ``'gaussian'``, ``'constgaussian'``}
        :r:     - Fuzzy function parameters, a 1 element scalar or a 2 element vector of positive values. 
                The ``r`` parameters for each fuzzy  function are defined as follows:   [default: (.2 2)]
                  - default:      [Tuple]
                      * r(1) = divisor of the exponential argument
                      * r(2) = argument exponent (pre-division)  
                  - sigmoid:      [Tuple]
                      * r(1) = divisor of the exponential argument
                      * r(2) = value subtracted from argument (pre-division)
                  - modsampen:    [Tuple]
                      * r(1) = divisor of the exponential argument
                      * r(2) = value subtracted from argument (pre-division)
                  - gudermannian:   
                      * r  = a scalar whose value is the numerator of  argument to gudermannian function: GD(x) = atan(tanh(r/x)). GD(x) is normalised to have a maximum value of 1.
                  - triangular:  
                      * r = a scalar whose value is the threshold (corner point) of the triangular function.
                  - trapezoidal1:  
                      * r = a scalar whose value corresponds to the upper (2r) and lower (r) corner points of the trapezoid.
                  - trapezoidal2:  [Tuple]
                      * r(1) = a value corresponding to the upper corner point of the trapezoid.
                      * r(2) = a value corresponding to the lower corner point of the trapezoid.
                  - z_shaped:  
                      * r = a scalar whose value corresponds to the upper (2r) and lower (r) corner points of the z-shape.
                  - bell:  
                      * r(1) = divisor of the distance value
                      * r(2) = exponent of generalized bell-shaped function
                  - gaussian:  
                      * r = a scalar whose value scales the slope of the Gaussian curve.
                  - constgaussian:  
                      * r = a scalar whose value defines the lower threshod and shape of the Gaussian curve.                    
                  - [DEPRICATED] linear:       
                      r  = an integer value. When r = 0, the argument of the exponential function is 
                      normalised between [0 1]. When r = 1, the minimuum value of the exponential argument is set to 0.    
        :Logx:  - Logarithm base, a positive scalar  [default: natural]
    
    For further information on the keyword arguments, see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``FuzzEn``, ``XSampEn``, ``XApEn``, ``FuzzEn2D``, ``XMSEn``, ``MSEn``
    
    :References:
        [1] Hong-Bo Xie, et al.,
            "Cross-fuzzy entropy: A new method to test pattern synchrony of
            bivariate time series." 
            Information Sciences 
            180.9 (2010): 1715-1724.
            
        [2] Hamed Azami, et al.
            "Fuzzy Entropy Metrics for the Analysis of Biomedical Signals: 
            Assessment and Comparison"
            IEEE Access
            7 (2019): 104833-104847
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
        
    N  = S1.shape[0]
    N2 = S2.shape[0]     
    assert N>10 and N2>10,  "Sig1/Sig2:   Each sequence must be a numpy vector (N>10)"
    assert isinstance(m,int) and (m>0), "m:     must be an integer > 0"
    assert isinstance(tau,int) and (tau>0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) or ((r[0] >= 0) and len(r) ==2), "r:     must be 2 element tuple of positive values"    
    assert Fx.lower() in ['default','sigmoid','modsampen','gudermannian', 'bell', 
                          'gaussian', 'constgaussian', 'triangular' , 
                          'trapezoidal1', 'trapezoidal2', 'z_shaped'] \
            and isinstance(Fx,str), """Fx:    must be one of the following strings -
            'default', 'sigmoid', 'modsampen', 'gudermannian', 'bell', 'z_shaped',
            'triangular', 'trapezoidal1','trapezoidal2','gaussian','constgaussian'"""
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    
    if isinstance(r,tuple) and Fx.lower()=='linear':
        r = 0
        print('Multiple values for r entered. Default value (0) used.') 
    elif isinstance(r,tuple) and Fx.lower()=='gudermannian':
        r = r[0];
        print('Multiple values for r entered. First value used.')      
        
    m = m+1      
    Fun = globals()[Fx.lower()]   
    Sx1 = np.zeros((N,m))
    Sx2 = np.zeros((N2,m))    
    for k in range(m):
        Sx1[:N-k*tau,k] = S1[k*tau::]
        Sx2[:N2-k*tau,k] = S2[k*tau::]
        
    Ps1 = np.zeros(m)
    Ps2 = np.zeros(m-1)
    Ps1[0] = 1    
    for k in range(2,m+1):        
        N1x = N - k*tau
        N2x = N - (k-1)*tau        
        N1y = N2 - k*tau
        N2y = N2 - (k-1)*tau
                
        A = Sx1[:N2x,:k] - np.transpose(np.tile(np.mean(Sx1[:N2x,:k],axis=1),(k,1)))
        B = Sx2[:N2y,:k] - np.transpose(np.tile(np.mean(Sx2[:N2y,:k],axis=1),(k,1)))
        d2 = np.zeros((N2x,N2y))        
                    
        for p in range(N2x):
            Mu2 = np.max(np.abs(A[p,:] - B),axis=1)
            d2[p,:] = Fun(Mu2,r)   
        
        Ps1[k-1] = np.mean(d2[:N1x,:N1y])
        Ps2[k-2] = np.mean(d2)
        
    # m = m+1      
    # Fun = globals()[Fx.lower()]   
    # Sx1 = np.zeros((N,m))
    # Sx2 = np.zeros((N,m))    
    # for k in range(m):
    #     Sx1[:N-k*tau,k] = S1[k*tau::]
    #     Sx2[:N-k*tau,k] = S2[k*tau::]
        
    # Ps1 = np.zeros(m)
    # Ps2 = np.zeros(m-1)
    # Ps1[0] = 1    
    # for k in range(2,m+1):        
    #     N1 = N - k*tau
    #     N2 = N - (k-1)*tau
    #     A = Sx1[:N2,:k] - np.transpose(np.tile(np.mean(Sx1[:N2,:k],axis=1),(k,1)))
    #     B = Sx2[:N2,:k] - np.transpose(np.tile(np.mean(Sx2[:N2,:k],axis=1),(k,1)))
    #     d2 = np.zeros((N2,N2))        
                    
    #     for p in range(N2):
    #         Mu2 = np.max(np.abs(A[p,:] - B),axis=1)
    #         d2[p,:] = Fun(Mu2,r)   
        
    #     Ps1[k-1] = np.mean(d2[:N1,:N1])
    #     Ps2[k-2] = np.mean(d2)
        
    with np.errstate(divide='ignore', invalid='ignore'):
        XFuzz = (np.log(Ps1[:-1]) - np.log(Ps2))/np.log(Logx)
        
    return XFuzz, Ps1, Ps2   

def sigmoid(x,r):
    assert isinstance(r,tuple), 'When Fx = "Sigmoid", r must be a two-element tuple.'
    y = 1/(1 + np.exp((x-r[1])/r[0]))
    return y  
def default(x,r):   
    assert isinstance(r,tuple), 'When Fx = "Default", r must be a two-element tuple.'
    y = np.exp(-(x**r[1])/r[0])
    return y     
def modsampen(x,r):
    assert isinstance(r,tuple), 'When Fx = "Modsampen", r must be a two-element tuple.'
    y = 1/(1 + np.exp((x-r[1])/r[0]));
    return y    
def gudermannian(x,r):
    if r <= 0:
        raise Exception('When Fx = "Gudermannian", r must be a scalar > 0.')
    y = np.arctan(np.tanh(r/x))    
    y = y/np.max(y)    
    return y    
# def linear(x,r):    
#     if r == 0 and x.shape[0]>1:    
#         y = np.exp(-(x - min(x))/np.ptp(x))
#     elif r == 1:
#         y = np.exp(-(x - min(x)))
#     elif r == 0 and x.shape[0]==1:   
#         y = 0;
#     else:
#         print(r)
#         raise Exception('When Fx = "Linear", r must be 0 or 1')
#     return y
def triangular(x, r):
    assert np.size(r)==1, 'When Fx = "Triangular", r must be a scalar > 0.'
    y = 1 - (x/r)
    y[x > r] = 0
    return y
def trapezoidal1(x, r):
    assert np.size(r)==1, 'When Fx = "Trapezoidal1", r must be a scalar > 0.'
    y = np.zeros(np.shape(x))
    y[x <= r*2] = 2 - (x[x <= r*2]/r)
    y[x <= r] = 1
    return y
def trapezoidal2(x, r):
    assert isinstance(r,tuple), 'When Fx = "Trapezoidal2", r must be a two-element tuple.'
    y = np.zeros(np.shape(x))
    y[x <= max(r)] = 1 - (x[x <= max(r)] - min(r))/(max(r)-min(r))
    y[x <= min(r)] = 1
    return y
def z_shaped(x, r):
    assert np.size(r)==1, 'When Fx = "Z_shaped", r must be a scalar > 0.'
    y = np.zeros(np.shape(x))
    y[x <= 2*r] = 2*(((x[x <= 2*r] - 2*r)/r)**2)
    y[x <= 1.5*r] = 1 - (2*(((x[x <= 1.5*r] - r)/r)**2))
    y[x <= r] = 1
    return y
def bell(x, r):
    assert isinstance(r,tuple), 'When Fx = "Bell", r must be a two-element tuple.'
    y = 1/(1 + abs(x/r[0])**(2*r[1]))
    return y
def gaussian(x, r):
    assert np.size(r)==1, 'When Fx = "Gaussian", r must be a scalar > 0.'
    y = np.exp(-((x**2)/(2*(r**2))))
    return y
def constgaussian(x, r):
    assert np.size(r)==1, 'When Fx = "ConstGaussian", r must be a scalar > 0.'
    y = np.ones(np.shape(x))
    y[x > r] = np.exp(-np.log(2)*((x[x > r] - r)/r)**2)
    return y

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