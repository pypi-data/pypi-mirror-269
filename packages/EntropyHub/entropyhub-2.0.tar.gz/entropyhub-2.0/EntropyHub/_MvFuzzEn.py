""" Base Multivariate Fuzzy Entropy function."""
import numpy as np       

def MvFuzzEn(Data, m=None, tau=None, r=(0.2,2.0), Fx='default', Norm=False, Logx=np.exp(1)):
    """MvFuzzEn  estimates the multivariate fuzzy entropy of a multivariate dataset.

    .. code-block:: python
    
        MFuzz, B0, Bt, B1 = MvFuzzEn(Data) 

    Returns the multivariate fuzzy entropy estimate (``MFuzz``) and the 
    average vector distances (``m``: ``B0``; joint total 
    ``m+1`` subspace: ``Bt``; all possible ``m+1`` subspaces: ``B1``),
    from the M multivariate sequences in ``Data`` using the default parameters: 
    embedding dimension = 2*np.ones(M,1), time delay = np.ones(M,1), 
    fuzzy membership function = "default", fuzzy function parameters= [0.2, 2],
    logarithm = natural, data normalization = false,     
    
    .. attention::

        The entropy value returned as ``MFuzz`` is estimated using the "full" 
        method [i.e.  -log(Bt/B0)] which compares delay vectors across all possible ``m+1`` 
        expansions of the embedding space as applied in [1][3]. Contrary to
        conventional definitions of sample entropy, this method does not provide a
        lower bound of 0!!
        Thus, it is possible to obtain negative entropy values for multivariate 
        fuzzy entropy, even for stochastic processes...
        
        Alternatively, one can calculate ``MFuzz`` via the "naive" method, 
        which ensures a lower bound of 0, by using the average vector distances
        for an individual ``m+1`` subspace (B1) [e.g. -log(B1(1)/B0)],
        or the average for all ``m+1`` subspaces [i.e. -log(mean(B1)/B0)].

    .. note::
        
        To maximize the number of points in the embedding process, this algorithm 
        uses N-max(m*tau) delay vectors and **not** N-max(m)*max(tau) as employed 
        in [1] and [3].
    
    
    .. code-block:: python
    
        MFuzz, B0, Bt, B1 = MvFuzzEn(Data, name, value, ...)

    Returns the multivariate fuzzy entropy estimates (``MFuzz``) estimated 
    from the M multivariate data sequences in ``Data`` using the specified
    keyword arguments:
        :Data:  - Multivariate dataset, NxM matrix of N (>10) observations (rows) and M (cols) univariate data sequences 
        :m:     - Embedding Dimension, a vector of M positive integers
        :tau:   - Time Delay, a vector of M positive integers
        :Fx:    - Fuzzy function name, one of the following strings:
              {``'sigmoid'``, ``'modsampen'``, ``'default'``, ``'gudermannian'``, ``'bell'``, ``'triangular'``, ``'trapezoidal1'``, ``'trapezoidal2'``, ``'z_shaped'``, ``'gaussian'``, ``'constgaussian'``}
        :r:     - Fuzzy function parameters, a 1 element scalar or a 2 element vector of positive values. The ``r`` parameters for each fuzzy  function are defined as follows  (default: [.2 2])
                      :sigmoid:     
                                  * r(1) = divisor of the exponential argument
                                  * r(2) = value subtracted from argument (pre-division)
                      :modsampen:    
                                  *  r(1) = divisor of the exponential argument
                                  *  r(2) = value subtracted from argument (pre-division)
                      :default:      
                                  *  r(1) = divisor of the exponential argument
                                  *  r(2) = argument exponent (pre-division)
                      :gudermannian: 
                                  *  r  = a scalar whose value is the numerator of argument to gudermannian function - GD(x) = atan(tanh(r/x)). 
                                     GD(x) is normalised to have a maximum value of 1.                       
                      :triangular:  
                                  * r = a positive scalar whose value is the threshold 
                                    (corner point) of the triangular function.
                      :trapezoidal1:  
                                  * r = a positive scalar whose value corresponds
                                    to the upper (2r) and lower (r) corner points of the trapezoid.
                      :trapezoidal2:  
                                  * r(1) = a value corresponding to the upper corner point of the trapezoid.
                                  * r(2) = a value corresponding to the lower corner point of the trapezoid.
                      :z_shaped:  
                                  * r = a scalar whose value corresponds to the
                                    upper (2r) and lower (r) corner points of the z-shape.
                      :bell:  
                                  * r(1) = divisor of the distance value
                                  * r(2) = exponent of generalized bell-shaped function
                      :gaussian:  
                                  * r = a scalar whose value scales the slope of the Gaussian curve.
                      :constgaussian:  
                                  * r = a scalar whose value defines the lower 
                                    threshod and shape of the Gaussian curve.
        :Norm:  - Normalisation of all M sequences to unit variance, a boolean
        :Logx:  - Logarithm base, a positive scalar  [default: natural]
      
    For further information on the keyword arguments, see the `EntropyHub guide <https://github.com/MattWillFlood/EntropyHub/blob/main/EntropyHub%20Guide.pdf>`_.
    
    :See also:
        ``MvSampEn``, ``FuzzEn``, ``XFuzzEn``, ``FuzzEn2D``, ``MSEn``, ``MvPermEn``.
    
    :References:
       [1] Ahmed, Mosabber U., et al. 
            "A multivariate multiscale fuzzy entropy algorithm with application
            to uterine EMG complexity analysis." 
            Entropy 19.1 (2016): 2.
    
       [2] Azami, Alberto Fernández, Javier Escudero. 
            "Refined multiscale fuzzy entropy based on standard deviation for 
            biomedical signal analysis." 
            Medical & biological engineering & computing 55 (2017): 2037-2052.
    
       [3] Ahmed Mosabber Uddin, Danilo P. Mandic
            "Multivariate multiscale entropy analysis."
            IEEE signal processing letters 19.2 (2011): 91-94.
    """
   
    Data = np.squeeze(Data)
    assert Data.shape[0]>10 and Data.ndim==2 and Data.shape[1]>1,  "Data:   must be an NxM numpy matrix where N>10 and M>1"
    N, Dn = Data.shape 
    if m is None:    m = 2*np.ones(Dn, dtype=int)
    if tau is None:  tau = np.ones(Dn, dtype=int)
    m = m.astype(int)
    tau = tau.astype(int) 
  
    assert isinstance(m,np.ndarray) and all(m>0) and m.size==Dn and m.ndim==1, "m:     must be numpy vector of M positive integers"
    assert isinstance(tau,np.ndarray) and all(tau>0) and tau.size==Dn and tau.ndim==1, "tau:   must be numpy vector of M positive integers"
    assert isinstance(r,(int,float)) or ((r[0] >= 0) and len(r) ==2), "r:     must be a scalar or 2 element tuple of positive values"
    assert Fx.lower() in ['default','sigmoid','modsampen','gudermannian',
                          'bell', 'gaussian', 'constgaussian', 'triangular' ,
                          'trapezoidal1', 'trapezoidal2', 'z_shaped'] \
            and isinstance(Fx,str), """Fx:    must be one of the following strings -
            'default', 'sigmoid', 'modsampen', 'gudermannian', 'bell', 'z_shaped',
            'triangular', 'trapezoidal1','trapezoidal2','gaussian','constgaussian'"""
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Norm,bool), "Norm:     must be a Boolean"    

    if Norm: Data = Data/np.std(Data,axis=0)
    
    Fun = globals()[Fx.lower()]       
    Nx = N - max((m-1)*tau)
    Ny = N - max(m*tau)
    Vex = np.zeros((Nx,sum(m)))
    q = 0
    for k in range(Dn):
        for p in range(m[k]):
            Vex[:,q] = Data[p*tau[k]:Nx+p*tau[k],  k]
            q += 1
            
    Count0 = Distx(Vex - np.mean(Vex,axis=1,keepdims=True), r, Fun)
    B0 = np.sum(Count0)/(Nx*(Nx-1)/2)
            
    B1 = np.zeros(Dn)
    Vez = np.inf*np.ones((1,sum(m)+1));
    Temp = np.cumsum(m)
    for k in range(Dn):
        Sig = np.expand_dims(Data[m[k]*tau[k]:Ny+m[k]*tau[k], k],1)
        Vey = np.hstack((Vex[:Ny, :Temp[k]], Sig, Vex[:Ny, Temp[k]:]))
        Vez = np.vstack((Vez, Vey))
        Count1 = Distx(Vey - np.mean(Vey,axis=1,keepdims=True), r, Fun)
        B1[k] = np.sum(Count1)/(Ny*(Ny-1)/2)
    Vez = Vez[1:,:]
    Count1 = Distx(Vez - np.mean(Vez,axis=1,keepdims=True), r, Fun)
    Bt = np.sum(Count1)/(Dn*Ny*((Dn*Ny)-1)/2)
       
    with np.errstate(divide='ignore', invalid='ignore'):
        MFuzz = -np.log(Bt/B0)/np.log(Logx) 
   
    return MFuzz, B0, Bt, B1    


def Distx(Vex, r, Fun):
    Nt = Vex.shape[0]
    Counter = np.zeros((Nt-1,Nt-1))
    for x in range(Nt-1):
        Counter[x,x:] = Fun(np.max(abs(Vex[x+1:,:] - Vex[x,:]), axis=1), r)
    return Counter


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