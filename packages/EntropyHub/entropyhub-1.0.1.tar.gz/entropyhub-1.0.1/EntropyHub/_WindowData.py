"""WindowData restructures a univariate/multivariate dataset into a collection of subsequence windows."""
import numpy as np 

def WindowData(Data, WinLen=None, Overlap=0, Mode="exclude"):
    """WindowData restructures a univariate/multivariate dataset into a collection of subsequence windows.

    .. code-block:: python

       WinData, Log = WindowData(Data) 
 
   Windows the sequence(s) given in ``Data`` into a collection of subsequnces  
   of floor(N/5) elements with no overlap, excluding any remainder
   elements that do not fill the final window.
   If ``Data`` is a univariate sequence (vector), ``Windata`` is a tuple of 5
   vectors. If ``Data`` is a set of multivariate sequences (NxM matrix), 
   each of M columns is treated as a sequence with N elements 
   and ``WinData`` is a tuple of 5 matrices of size [(floor*N,5), M]. 
   The ``Log`` dictionary contains information about the windowing process, including:
       :DataType:      - The type of data sequence passed as ``Data``
       :DataLength:    - The number of sequence elements in ``Data``
       :WindowLength:  - The number of elements in each window of ``WinData``
       :WindowOverlap: - The number of overlapping elements between windows
       :TotalWindows:  - The number of windows extracted from ``Data`` 
       :Mode:          - Decision to include or exclude any remaining sequence elements (``< WinLen``) that do not fill the window.
 
    .. code-block:: python

       WinData, Log = WindowData(Data, keyword = value, ...)
 
   Windows the sequence(s) given in ``Data`` into a collection of subsequnces
   using the specified keyword arguments: 
       :WinLen:  - Number of elements in each window, a positive integer (>10)
       :Overlap: - Number of overlapping elements between windows, a positive integer (< WinLen)
       :Mode:    - Decision to include or exclude any remaining sequence elements (< ``WinLen``) that do not fill the window, a string - either ``"include"`` or ``"exclude"`` (default).

   :See also:
       ``ExampleData``

    """
               
    Data = np.squeeze(Data)
    assert isinstance(Data,np.ndarray) and Data.shape[0]>10 and Data.ndim<=2,  "Data:   must be a numpy Vector (length N) or an NxM numpy matrix where N>10 and M>1"

    if Data.ndim == 1:   
        DataType =  "single univariate vector (1 sequence)"
        N = Data.shape[0]; Dn = 0 
    elif Data.ndim == 2: 
        N, Dn = Data.shape 
        DataType = "multivariate matrix (" +str(Dn)+" vectors)"

    if WinLen is None: WinLen = N//5
    assert isinstance(WinLen,int)  and WinLen<N and WinLen>10, "WinLen: must be an integer such that 10 < WinLen < N"
    assert isinstance(Overlap,int) and Overlap>=0 and Overlap<WinLen, "Overlap: The number of overlapping window samples such that 0 <= Overlap < WinLen"
    assert isinstance(Mode, str) and  Mode.lower() in ["exclude","include"], "Mode: Option to include/exclude samples that do not fill final window, either 'exclude' or 'include'"
        
    if Dn==0:  Data = np.expand_dims(Data, 1)
    M = (N - Overlap)//(WinLen - Overlap)
    Step = WinLen-Overlap
    Xout = []
    for k in range(0,M*Step,Step):
        Xout.append(np.squeeze(Data[k:k+WinLen,:]))   
    
    if (Mode.lower() == "include") and (len(Xout)-1)*Step+WinLen!=N:   
        Xout.append(np.squeeze(Data[k+Step:,:])); M+=1
    
    WinData = tuple(Xout)
    Log = {"DataType": DataType, "DataLength": N, "WindowLength": WinLen,
           "WindowOverlap": Overlap,  "TotalWindows": M,   "Mode": Mode}
    
    return WinData, Log


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