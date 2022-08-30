from libcpp.vector cimport vector
from tesseract5 cimport *
cdef extern from "Tetragon.cpp":
    pass

cdef extern from "FromPicture.h":
    pass

cdef extern from "FromPicture.cpp":
    pass

cdef extern from "FromPicture.h" namespace "robert":
    cdef cppclass FromPicture:
        FromPicture() except +
        FromPicture(Pix *) except +

cdef extern from "Tetragon.h" namespace "robert":
    cdef cppclass Tetragon:
        Tetragon() except +
        Tetragon(int, int, int, int, int, int, int, int) except +
        void ThresholdTetragonToPix(FromPicture , int *, int *, int *) except +
        void OtsuThresholdTetragon(FromPicture, int *, int *, int *) except +



