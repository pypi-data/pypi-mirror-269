"""Base Bidimensional Sample Entropy function."""
import numpy as np    

def SampEn2D(Mat, m=None, tau=1, r=None, Logx=np.exp(1), Lock=True):
    """SampEn2D  Estimates the bidimensional sample entropy of a data matrix.

    .. code-block:: python
    
        SE2D, Phi1, Phi2 = SampEn2D(Mat) 
        
    Returns the bidimensional sample entropy estimate (``SE2D``) and the number
    of matched sub-matricess (``m: Phi1``, ``m+1: Phi2``) estimated for the data 
    matrix (Mat) using the default parameters: time delay = 1,
    radius distance threshold = 0.2*SD(``Mat``), logarithm = natural
    matrix template size = [floor(H/10) floor(W/10)]  (where H and W represent
    the height (rows) and width (columns) of the data matrix ``Mat``) 
    * The minimum dimension size of Mat must be > 10.
 
     .. code-block:: python
     
         SE2D, Phi1, Phi2 = SampEn2D(Mat, keyword = value, ...)
    
    Returns the bidimensional sample entropy (``SE2D``) estimates for the data
    matrix (``Mat``) using the specified 'keyword' arguments:
        :m:     - Template submatrix dimensions, an integer scalar (for sub-matrix with same height and width) or a two-element tuple of integers (height, width) with a minimum value > 1. (default: [floor(H/10) floor(W/10)])
        :tau:   - Time Delay, a positive integer > 1   (default: 1)
        :r:     - Distance Threshold, a positive scalar   (default: 0.2*SD(``Mat``))
        :Logx:  - Logarithm base, a positive scalar    (default: natural)        
        :Lock:  - By default, ``SampEn2D`` only permits matrices with a maximum  size of 128 x 128 to prevent RAM overload. 
              e.g. For ``Mat`` = [200 x 200], ``m`` = 3, and ``tau`` = 1, ``SampEn2D`` 
              creates a vector of 753049836 elements. To enable matrices greater than [128 x 128] elements, set ``Lock = False`` (default: True)
              ``CAUTION: unlocking the permitted matrix size may cause memory``
              ``errors that could lead your Python IDE to crash.``
    
    :See also:
        ``SampEn``, ``FuzzEn2D``, ``DistEn2D``, ``XSampEn``, ``MSEn``
    
    :References:
        [1] Luiz Eduardo Virgili Silva, et al.,
            "Two-dimensional sample entropy: Assessing image texture 
            through irregularity." 
            Biomedical Physics & Engineering Express
            2.4 (2016): 045002.
    """
            
    Mat = np.squeeze(Mat)
    NL,NW = Mat.shape    
    if m is None:
        m = np.array(Mat.shape)//10
    if r == None:
        r = 0.2*np.std(Mat)
           
    assert Mat.ndim==2 and min(Mat.shape)>10 , \
    "Mat:   must be a 2D numpy array with height & width > 10"
    assert (isinstance(m,int) and m>1) or (isinstance(m, (np.ndarray,tuple))  
                                           and len(m)==2 and min(m)>1), \
    "m:     must be an integer > 1, or a 2 element tuple of integers > 1"
    assert isinstance(tau,int) and (tau > 0), "tau:   must be an integer > 0"
    assert isinstance(r,(int,float)) and r>0, "r:     must be a positive value"
    assert isinstance(Logx,(int,float)) and (Logx>0), "Logx:     must be a positive value"
    assert isinstance(Lock,bool) and ((Lock==True and max(Mat.shape)<=128) or Lock==False), \
    "Lock:      To prevent memory storage errors, matrix width & length must \
    have <= 128 elements. To estimate SampEn2D for the current matrix (%d x %d) \
    change Lock to False. \
    CAUTION: unlocking the permitted matrix size may cause memory \
    errors that could lead your Python IDE to crash.."%(NW,NL)
    
    if isinstance(m,int):
        mL = int(m); mW = int(m)        
    else:
        mL = int(m[0]); mW = int(m[1])       
                
    NL = NL - mL*tau
    NW = NW - mW*tau
    X = np.zeros((NL*NW,mL+1,mW+1))
    p = 0
    for k in range(NL):        
        for n in range(NW):
            X[p,:,:] = Mat[k:(mL+1)*tau+k:tau,n:(mW+1)*tau+n:tau]
            p += 1           
                        
    if p != NL*NW:
        print('Warning: Potential error with submatrix division.')        
    Ny = int(p*(p-1)/2)
    if Ny > 300000000:
        print('Warning: Number of pairwise distance calculations is ' + str(Ny))
        
    Y1 = np.zeros(p-1, dtype=int)
    Y2 = np.zeros(p-1, dtype=int)
    for k in range(p-1):
        Temp = (np.max(abs(X[k+1:,:-1,:-1] - X[k,:-1,:-1]),axis=(1,2)) < r)
        Y1[k] = sum(Temp)        
        Temp = np.where(Temp==True)[0] + k + 1
        Y2[k] = sum(np.max(abs(X[Temp,:,:] - X[k,:,:]),axis=(1,2)) < r)
     
    Phi1 = sum(Y1)/Ny
    Phi2 = sum(Y2)/Ny
    SE2D = -np.log(Phi2/Phi1)/np.log(Logx)
    
    return SE2D, (Phi1,Phi2)


    # ix = np.vstack((np.repeat(np.arange(NL),NW), np.tile(np.arange(NW),NL))).T
    # T1a, T2a = [],[]
    # T1b, T2b = [],[]
    # Y1 = np.zeros(p-1,dtype=int)
    # Y2 = np.zeros(p-1,dtype=int)
    # for k in range(p-1):
    #     Temp = (np.max(abs(X[k+1:,:-1,:-1] - X[k,:-1,:-1]), axis=(1,2)) < r)
    #     Y1[k] = Temp.sum()        
    #     T1b.extend(np.tile(ix[k].T,(Y1[k],1)))
    #     T2b.extend(ix[k+1:,:][Temp,:])
                    
    #     Temp2 = np.where(Temp)[0] + k + 1
    #     Temp3 = (np.max(abs(X[Temp2,:,:] - X[k,:,:]), axis=(1,2)) < r)
    #     Y2[k] = sum(Temp3)
    #     T1a.extend(np.tile(ix[k].T,(Y2[k],1)))
    #     T2a.extend(ix[Temp2[Temp3],:])
    
    # Phi1 = sum(Y1)/Ny
    # Phi2 = sum(Y2)/Ny
    # SE2D = -np.log(Phi2/Phi1)/np.log(Logx)
    
    # T1a = np.asarray(T1a);     T2a = np.asarray(T2a)
    # T1b = np.asarray(T1b);     T2b = np.asarray(T2b)    
    
    # Ka = 0
    # for k in range(len(T1a)):
    #     Ka += int(((abs(T2a[:,0]- T1a[k,0]) < (mL+1)*tau) + 
    #            (abs(T2a[:,1]- T1a[k,1]) < (mW+1)*tau)).sum())
        
    # Kb = 0
    # for k in range(len(T1b)):
    #     Kb += int(((abs(T2b[:,0]- T1b[k,0]) < mL*tau) + 
    #            (abs(T2b[:,1]- T1b[k,1]) < mW*tau)).sum())
        

    # # TaL = (abs(np.expand_dims(T1a[:,0],axis=1) - np.expand_dims(T2a[:,0],axis=0)) < (mL+1)*tau)
    # # TaW = (abs(np.expand_dims(T1a[:,1],axis=1) - np.expand_dims(T2a[:,1],axis=0)) < (mW+1)*tau)    
    # # Ka = (TaL + TaW).sum()
    
    # # TbL = (abs(np.expand_dims(T1b[:,0],axis=1) - np.expand_dims(T2b[:,0],axis=0)) < mL*tau)
    # # TbW = (abs(np.expand_dims(T1b[:,1],axis=1) - np.expand_dims(T2b[:,1],axis=0)) < mW*tau)    
    # # Kb = (TbL + TbW).sum()
        
    
    # CP = Y1.sum()/Y2.sum()
    # Vcp = (CP*(1-CP)/Y2.sum()) + (Ka - Kb*(CP**2))/(Y2.sum()**2)
    # return SE2D, (Phi1, Phi2), (Vcp, Ka, Kb)


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