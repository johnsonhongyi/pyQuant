import numpy as np
import scipy as sp
import numba as nb
# from cython_resample import cython_resample

@nb.autojit
def numba_resample(qs, xs, rands):
    n = qs.shape[0]
    lookup = np.cumsum(qs)
    results = np.empty(n)

    for j in range(n):
        for i in range(n):
            if rands[j] < lookup[i]:
                results[j] = xs[i]
                break
    return results

def python_resample(qs, xs, rands):
    n = qs.shape[0]
    lookup = np.cumsum(qs)
    results = np.empty(n)

    for j in range(n):
        for i in range(n):
            if rands[j] < lookup[i]:
                results[j] = xs[i]
                break
    return results

def numpy_resample(qs, xs, rands):
    results = np.empty_like(qs)
    lookup = sp.cumsum(qs)
    for j, key in enumerate(rands):
        i = sp.argmax(lookup>key)
        results[j] = xs[i]
    return results

#The following is the code for the cython module. It was compiled in a
#separate file, but is included here to aid in the question.
"""
import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64

ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
def cython_resample(np.ndarray[DTYPE_t, ndim=1] qs, 
             np.ndarray[DTYPE_t, ndim=1] xs, 
             np.ndarray[DTYPE_t, ndim=1] rands):
    if qs.shape[0] != xs.shape[0] or qs.shape[0] != rands.shape[0]:
        raise ValueError("Arrays must have same shape")
    assert qs.dtype == xs.dtype == rands.dtype == DTYPE

    cdef unsigned int n = qs.shape[0]
    cdef unsigned int i, j 
    cdef np.ndarray[DTYPE_t, ndim=1] lookup = np.cumsum(qs)
    cdef np.ndarray[DTYPE_t, ndim=1] results = np.zeros(n, dtype=DTYPE)

    for j in range(n):
        for i in range(n):
            if rands[j] < lookup[i]:
                results[j] = xs[i]
                break
    return results
"""
if __name__ == '__main__':
    n = 100
    xs = np.arange(n, dtype=np.float64)
    qs = np.array([1.0/n,]*n)
    rands = np.random.rand(n)
    import timeit
    # print "Timing Numba Function:"
    number = 1000
    ti = timeit.timeit(lambda :numba_resample(qs, xs, rands),number=number)
    print "Timing numba_resample Function:",ti
    # %timeit python_resample(qs, xs, rands)
    ti = timeit.timeit(lambda :python_resample(qs, xs, rands),number=number)
    print "Timing python_resample Function:",ti
    ti = timeit.timeit(lambda :numpy_resample(qs, xs, rands),number=number)
    print "Timing numpy_resample Function:",ti
    # %timeit cython_resample(qs, xs, rands)