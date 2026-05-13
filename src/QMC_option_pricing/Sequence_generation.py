import numpy as np


def Kronecker(m,n):
    """
    Generates a mxn array of points using Kronecker sequences (golden ratio conjugate)
    """
    n = int(n)
    m = int(m)

    alpha = (np.sqrt(5)-1)/2
    V = alpha * np.arange(m*n) % 1.0
    return V.reshape(n,m).T

def Halton(m,n,base=2):
    """
    Generates a mxn array of points using scrambled Van Der Corput sequence
    """
    n = int(n)
    m = int(m)

    indices = np.arange(1,m*n + 1)
    V = np.zeros(m*n)

    denom = 1.0

    while np.any(indices > 0):
        indices, remainder = np.divmod(indices, base)
        denom *= base
        V += remainder / denom
    
    np.random.permutation(V)

    return V.reshape(n,m).T

def Sobol(m,n,skip=100):
    """
    Generates a mxn array of points using Sobol sequences
    """
    n = int(n)
    m = int(m)

    bits = 32
    dtype = np.uint64
    i = np.arange(skip, skip + m*n, dtype=dtype)
    tz = ((~i) & (i + 1))
    c = np.floor(np.log2(tz)).astype(np.uint32) + 1
    dirs = np.uint64(1) << (bits - c)
    x = np.bitwise_xor.accumulate(dirs)
    V = (x / float(1 << bits)).astype(np.float64)

    return V.reshape(n,m).T
