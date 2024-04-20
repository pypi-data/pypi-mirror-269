from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport subprocess_reference
from libc.limits cimport ULLONG_MAX


cpdef size_t array_get_int(atomic_bytearray array, subprocess_reference reference) except ?ULLONG_MAX
cpdef bytes array_get_bytes(atomic_bytearray array, subprocess_reference reference, trim=*)
cpdef void array_set_bytes(atomic_bytearray array, subprocess_reference reference, bytes data) except *
cpdef bytes array_get_and_set(atomic_bytearray array, subprocess_reference reference, bytes data, bint trim=*)
cpdef bytes array_compare_and_set_value(atomic_bytearray array, subprocess_reference reference, bytes i , bytes n , bint trim=*)
cpdef bytes array_add_and_fetch(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_sub_and_fetch(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_fetch_and_add(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_fetch_and_sub(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_fetch_and_and(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_fetch_and_or(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bytes array_fetch_and_xor(atomic_bytearray array, subprocess_reference reference, bytes n, bint trim=*)
cpdef bint array_bittest_and_set(atomic_bytearray array, subprocess_reference reference, char offset) except *
cpdef bint array_bittest_and_reset(atomic_bytearray array, subprocess_reference reference, char offset) except *

cdef class atomic_bytearray(atomic_object):
    cdef readonly char initial_length
    cpdef size_t get_int(self) except ?ULLONG_MAX
    cpdef bytes get_bytes(self, bint trim=*)
    cpdef void set_bytes(self, bytes data) except *
    cpdef bint array_bittest_and_set(self, char offset) except *
    cpdef bint array_bittest_and_reset(self, char offset) except *
    cpdef bytes array_get_and_set(self, bytes data, bint trim=*)
    cpdef bytes array_compare_and_set_value(self, bytes i, bytes n, bint trim=*)

    cpdef bytes array_add_and_fetch(self, bytes n, bint trim=*)
    cpdef bytes array_sub_and_fetch(self, bytes n, bint trim=*)
    cpdef bytes array_fetch_and_add(self, bytes n, bint trim=*)
    cpdef bytes array_fetch_and_sub(self, bytes n, bint trim=*)
    cpdef bytes array_fetch_and_and(self, bytes n, bint trim=*)
    cpdef bytes array_fetch_and_or(self, bytes n, bint trim=*)
    cpdef bytes array_fetch_and_xor(self, bytes n, bint trim=*)

