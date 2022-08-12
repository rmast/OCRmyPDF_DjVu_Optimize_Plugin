# distutils: language = c++
import tgon
from tesseract5 cimport *
import sys
from io import BytesIO
from cython.operator import dereference, preincrement
from libcpp.list cimport list as cpplist
cdef tuple _image_buffer(image):
    """Return raw bytes of a PIL Image"""
    with BytesIO() as f:
        # Pix and BMP only allow alpha as RGBA:
        if image.mode in ['LA', 'PA', 'RGBa', 'La']:
            image = image.convert('RGBA')
        image.save(f, image.format or 'BMP')
        num_channels = len(image.getbands())

        return f.getvalue(), num_channels

from Tetragon cimport Tetragon, FromPicture

cdef class PyRectangle:
    cdef FromPicture c_pict
    cdef Tetragon c_rect  # hold a pointer to the C++ instance which we're wrapping
    def __init__(self, image):
        cdef:
            cuchar_t *buff
            size_t size
            bytes raw
            int num_channels

        raw, num_channels = _image_buffer(image)
        buff = raw
        size = len(raw)

        with nogil:
            plaatje = pixReadMem(buff, size)
            if plaatje == NULL:
                with gil:
                    raise RuntimeError('Error reading image')
        self.c_pict = FromPicture(plaatje, num_channels)


    def otsu_threshold_tetragon(self, result): 
        cdef vector[int] thresholds, edgemean
        cdef cpplist[int].iterator it
        #cdef cpplist[].iterator a

        cdef int c0 
        cdef int c1
        cdef int c2
        cdef int c3

        for x in result[0]:
            for a in x:
                #it=a.begin()
                #c0 = dereference(it)
                #preincrement(it)
                #c1 = dereference(it)
                #preincrement(it)
                #c2 = dereference(it)
                #preincrement(it)
                #c3 = dereference(it)
                #print(c0)
                #print(c1)
                #print(c2)
                #print(c3)
                self.c_rect = Tetragon(a[0], a[2], a[0], a[3], a[1], a[3], a[1] , a[2])
                self.c_rect.OtsuThresholdTetragon(self.c_pict, thresholds, edgemean);
                #sys.stdout.write("Hello %s!" % thresholds)
                print(a,thresholds,edgemean)

        #for x in result[1]:
            #for a in x:
                #for b in a:
                    #rect_obj = tgon.PyRectangle(b.front(), b.back(), b[0], b[3], b[1], b[3], b[1], b[2])


        return thresholds, edgemean
