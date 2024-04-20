"""Base Bidimensional Fuzzy Entropy function."""
import numpy as np    

def FuzzEn2D(Mat, m=None, tau=1, r=None, Fx='default', Logx=np.exp(1), Lock=True):
    """FuzzEn2D  estimates the bidimensional fuzzy entropy of a data matrix.
 
    .. code-block:: python
    
        Fuzz2D = FuzzEn2D(Mat) 
        
    Returns the bidimensional fuzzy entropy estimate (``Fuzz2D``) estimated for 
    the data matrix (``Mat``) using the default parameters: time delay = 1,
    fuzzy function (``Fx``) = ``'default'``, fuzzy function parameters (``r``) = (0.2*SD(Mat), 2),
    logarithm = natural, matrix template size = [floor(H/10) floor(W/10)] 
    (where H and W represent the height (rows) and width (columns) of the data matrix ``'Mat'``) 
    ** The minimum number of rows and columns of Mat must be > 10.
 
    .. code-block:: python
    
        Fuzz2D = FuzzEn2D(Mat, keyword = value, ...)

    Returns the bidimensional fuzzy entropy (``Fuzz2D``) estimates for the data
    matrix (``Mat``) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer (for sub-matrix with same height and width) or a two-element vector of integers [height, width] with a minimum value > 1.  (default: [floor(H/10) floor(W/10)])
        :tau:   - Time Delay, a positive integer  (default: 1)
        :Fx:    - Fuzzy function name, one of the following strings:  
            {``'sigmoid'``, ``'modsampen'``, ``'default'``, ``'gudermannian'``, ``'bell'``, ``'triangular'``, ``'trapezoidal1'``, ``'trapezoidal2'``, ``'z_shaped'``, ``'gaussian'``, ``'constgaussian'``}
        :r:     - Fuzzy function parameters, a 1 element scalar or a 2 element vector of positive values. 
                The ``r`` parameters for each fuzzy  function are defined as follows:   [default: (0.2*SD(Mat), 2)]
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
                        
        :Logx:  - Logarithm base, a positive scalar    (default: natural)
        :Lock:  - By default, ``FuzzEn2D`` only permits matrices with a maximum  size of 128 x 128 to prevent RAM overload. 
                  e.g. For ``Mat`` = [200 x 200], ``m`` = 3, and ``tau`` = 1, ``FuzzEn2D`` 
                  creates a vector of 753049836 elements. To enable matrices greater than [128 x 128] elements, set ``Lock = False`` (default: True)
                  
                  ``CAUTION: unlocking the permitted matrix size may cause memory``
                  ``errors that could lead your Python IDE to crash.``
    
    :See also:
        ``SampEn2D``, ``DistEn2D``, ``FuzzEn``, ``XFuzzEn``, ``XMSEn``
    
    :References:
        [1] Luiz Fernando Segato Dos Santos, et al.,
            "Multidimensional and fuzzy sample entropy (SampEnMF) for
            quantifying H&E histological images of colorectal cancer."
            Computers in biology and medicine 
            103 (2018): 148-160.
    
        [2] Mirvana Hilal and Anne Humeau-Heurtier,
            "Bidimensional fuzzy entropy: Principle analysis and biomedical
            applications."
            41st Annual International Conference of the IEEE (EMBC) Society
            2019.
    
        [3] Hamed Azami, et al.
            "Fuzzy Entropy Metrics for the Analysis of Biomedical Signals: 
            Assessment and Comparison"
            IEEE Access
            7 (2019): 104833-104847
     """ 
    
    Mat = np.squeeze(Mat)
    NL,NW = Mat.shape     
    if m is None:
        m = np.array(Mat.shape)//10
    if r is None:
        r = (0.2*np.std(Mat), 2)

    assert Mat.ndim==2 and min(Mat.shape)>5 , \
    "Mat:   must be a 2D numpy array with height & width > 10"
    assert (isinstance(m,int) and m>1) or (isinstance(m, (np.ndarray,tuple))  
                                           and len(m)==2 and min(m)>1), \
    "m:     must be an integer > 1, or a 2 element tuple of integers > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) or ((r[0] >= 0) and len(r) ==2), "r:     must be 2 element tuple of positive values"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert Fx.lower() in ['default','sigmoid','modsampen','gudermannian', 'bell', 
                          'gaussian', 'constgaussian', 'triangular' , 
                          'trapezoidal1', 'trapezoidal2', 'z_shaped'] \
            and isinstance(Fx,str), """Fx:    must be one of the following strings -
            'default', 'sigmoid', 'modsampen', 'gudermannian', 'bell', 'z_shaped',
            'triangular', 'trapezoidal1','trapezoidal2','gaussian','constgaussian'"""
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate FuzzEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])   
    
    if isinstance(r,tuple) and Fx.lower()=='linear':
        r = 0
        print('Multiple values for r entered. Default value (0) used.') 
    elif isinstance(r,tuple) and Fx.lower()=='gudermannian':
        r = r[0];
        print('Multiple values for r entered. First value used.')     
        
    Fun = globals()[Fx.lower()]
    NL = NL - mL*tau
    NW = NW - mW*tau
    X1 = np.zeros((NL*NW,mL,mW))
    X2 = np.zeros((NL*NW,mL+1,mW+1))
    p = 0
    for k in range(NL):        
        for n in range(NW):
            Temp2 = Mat[k:(mL+1)*tau+k:tau,n:(mW+1)*tau+n:tau]
            Temp1 = Temp2[:-1,:-1]
            X1[p,:,:] = Temp1 - np.mean(Temp1)
            X2[p,:,:] = Temp2 - np.mean(Temp2)
            p += 1            
    if p != NL*NW:
        print('Warning: Potential error with submatrix division.')        
    Ny = int(p*(p-1)/2)
    if Ny > 300000000:
        print('Warning: Number of pairwise distance calculations is ' + str(Ny))
    
    Y1 = np.zeros(p-1)
    Y2 = np.zeros(p-1)
    for k in range(p-1):
        Temp1 = Fun(np.max(abs(X1[k+1:,:,:] - X1[k,:,:]),axis=(1,2)),r)
        Y1[k] = np.sum(Temp1)        
        Temp2 = Fun(np.max(abs(X2[k+1:,:,:] - X2[k,:,:]),axis=(1,2)),r)
        Y2[k] = np.sum(Temp2) 
        
    Fuzz2D = -np.log(sum(Y2)/sum(Y1))/np.log(Logx)
    return Fuzz2D


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