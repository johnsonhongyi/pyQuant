import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)


cpdef tuple cy_dd_custom_mv(double[:] ser):
    cdef double running_global_peak = ser[0]
    cdef double min_since_global_peak = ser[0]
    cdef double running_max_dd = 0

    cdef long running_global_peak_id = 0
    cdef long running_max_dd_peak_id = 0
    cdef long running_max_dd_trough_id = 0

    cdef long i
    cdef double val
    for i in xrange(ser.shape[0]):
        val = ser[i]
        if val >= running_global_peak:
            running_global_peak = val
            running_global_peak_id = i
            min_since_global_peak = val
        if val < min_since_global_peak:
            min_since_global_peak = val
            if val - running_global_peak <= running_max_dd:
                running_max_dd = val - running_global_peak
                running_max_dd_peak_id = running_global_peak_id
                running_max_dd_trough_id = i
    return (running_max_dd, running_max_dd_peak_id, running_max_dd_trough_id, running_global_peak_id)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def cy_rolling_dd_custom_mv(double[:] ser, long window):
    cdef double[:, :] result
    result = np.zeros((ser.shape[0], 4))
    print (result)
    cdef double running_global_peak = ser[0]
    cdef double min_since_global_peak = ser[0]
    cdef double running_max_dd = 0
    cdef long running_global_peak_id = 0
    cdef long running_max_dd_peak_id = 0
    cdef long running_max_dd_trough_id = 0
    cdef long i
    cdef double val
    cdef int prob_1
    cdef int prob_2
    cdef tuple intermed
    cdef long newthing

    for i in xrange(ser.shape[0]):
        val = ser[i]
        if i < window:
            if val >= running_global_peak:
                running_global_peak = val
                running_global_peak_id = i
                min_since_global_peak = val
            if val < min_since_global_peak:
                min_since_global_peak = val
                if val - running_global_peak <= running_max_dd:
                    running_max_dd = val - running_global_peak
                    running_max_dd_peak_id = running_global_peak_id
                    running_max_dd_trough_id = i

            result[i, 0] = <double>running_max_dd
            result[i, 1] = <double>running_max_dd_peak_id
            result[i, 2] = <double>running_max_dd_trough_id
            result[i, 3] = <double>running_global_peak_id

        else:
            prob_1 = 1 if result[i-1, 3] <= float(i - window) else 0
            prob_2 = 1 if result[i-1, 1] <= float(i - window) else 0
            if prob_1 or prob_2:
                intermed = cy_dd_custom_mv(ser[i-window+1:i+1])
                result[i, 0] = <double>intermed[0]
                result[i, 1] = <double>(intermed[1] + i - window + 1)
                result[i, 2] = <double>(intermed[2] + i - window + 1)
                result[i, 3] = <double>(intermed[3] + i - window + 1)
            else:
                newthing = <long>(int(result[i-1, 3]))
                result[i, 3] = i if ser[i] >= ser[newthing] else result[i-1, 3]
                if val - ser[newthing] <= result[i-1, 0]:
                    result[i, 0] = <double>(val - ser[newthing])
                    result[i, 1] = <double>result[i-1, 3]
                    result[i, 2] = <double>i
                else:
                    result[i, 0] = <double>result[i-1, 0]
                    result[i, 1] = <double>result[i-1, 1]
                    result[i, 2] = <double>result[i-1, 2]
    cdef double[:] finalresult = result[:, 0]
    return finalresult