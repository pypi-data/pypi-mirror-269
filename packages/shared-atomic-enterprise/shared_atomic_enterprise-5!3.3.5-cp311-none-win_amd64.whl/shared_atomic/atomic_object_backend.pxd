









































cdef class atomic_object:

    cdef readonly str mode
    cdef readonly size_t size
    cdef bint x3
    cdef long x4
    cdef long x5
    cdef int x6
    cdef long long x7
    cdef long long x8


    cdef dict x12
    cdef bytes y1(self, long long input, size_t length, bint threadlocal=*)
    cpdef void y2(self,
                                            object_id: int,
                                            bint windows_unix_compatibility,
                                            long long reference_m,
                                            size_t size,
                                            int creation_pid,
                                            size_t total_size_including_ending_zeros=*) except *
    cpdef void change_mode(self, str newmode=*, bint windows_unix_compatibility=*) except*
    cdef size_t y3(self, long long input)
    cdef long long y4(self, size_t input)
    cdef  void y5(self) except *
    cdef y6(self, bint windows_unix_compatibility)

cdef class subprocess_reference:
    cdef long long x1
    cdef long long x2

    cdef char y1(self) except? 0
    cdef void y2(self, char n) except*
    cdef char y3(self, char n) except? 0
    cdef char y4(self, char e, char n) except? 0
    cdef char y5(self, char n) except? 0
    cdef char y6(self, char n) except? 0
    cdef char y7(self, char n) except? 0
    cdef char y8(self, char n) except? 0
    cdef char y9(self, char n) except? 0

    cdef long long y10(self) except? 0
    cdef void y11(self, long long n) except*
    cdef long long y12(self, long long n) except? 0
    cdef long long y13(self, long long e, long long n)  except? 0
    cdef long long y14(self, long long n) except? 0
    cdef long long y15(self, long long n) except? 0
    cdef long long y16(self, long long n) except? 0
    cdef long long y17(self, long long n) except? 0
    cdef long long y18(self, long long n) except? 0
    cdef long long y19(self, long long n) except? 0
    cdef long long y20(self, long long n) except? 0
    cdef unsigned char y21(self, long long offset) except 2
    cdef unsigned char y22(self, long long offset) except 2
    cdef short y23(self) except? 0
    cdef void y24(self, short n) except*
    cdef short y25(self, short n) except? 0
    cdef short y27(self, short e, short n) except? 0

    cdef short y28(self, short n) except? 0
    cdef short y29(self, short n) except? 0
    cdef short y30(self, short n) except? 0
    cdef short y31(self, short n) except? 0
    cdef short y32(self, short n) except? 0

    cdef long y33(self) except? 0
    cdef void y34(self, long n) except*
    cdef long y35(self, long n) except? 0
    cdef long y36(self, long e, long n) except? 0
    cdef long y37(self, long n) except? 0
    cdef long y38(self, long n) except? 0
    cdef long y39(self, long n) except? 0
    cdef long y40(self, long n) except? 0
    cdef long y41(self, long n) except? 0
    cdef long y42(self, long n) except? 0
    cdef long y43(self, long n) except? 0
    cdef unsigned char y44(self, long offset) except 2
    cdef unsigned char y45(self, long offset) except 2
    cdef int y46(self, int size,
                                           char *i, int i_length, char * n, int n_length,
                                           char * out) except -1
    cdef int y47(self, char *i, char *n,
                                                         size_t offset, size_t size,
                                                         size_t total_size_including_ending_zeros, int length,
                                                         char * result) except -1




cdef class multiprocessing_reference(subprocess_reference):
    cdef long long x3
    cdef dict x4

    cdef void close_reference(self, bint windows_unix_compatibility) except *


cpdef subprocess_reference get_reference(atomic_object a)
cpdef void release_reference(subprocess_reference a) except *

cdef class array2d:
    cdef void * x1
    cdef bint x2
    cdef size_t x3
    cdef size_t x4
    cdef size_t x5
    cdef Py_ssize_t x6[2]
    cdef Py_ssize_t z7[2]
