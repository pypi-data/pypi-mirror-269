from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport subprocess_reference
from libc.limits cimport ULLONG_MAX

cpdef size_t list_get_int(atomic_list input_list, subprocess_reference reference) except ?ULLONG_MAX
cpdef void list_set_int(atomic_list input_list, subprocess_reference reference, size_t integer) except *
cpdef list list_get_list(atomic_list input_list, subprocess_reference reference)
cpdef void list_set_list(atomic_list input_list, subprocess_reference reference, list data) except *
cpdef list list_get_and_set(atomic_list input_list, subprocess_reference reference, list data)
cpdef list list_compare_and_set_value(atomic_list input_list, subprocess_reference reference, list i, list n)

cdef class atomic_list(atomic_object):
    cdef readonly char x13
    cdef readonly str x14
    cdef list l1(self, bytes bits_in_bytes)
    cdef tuple l2(self, list input_list)
    cdef tuple l3(self, size_t data_prefix, char accumulate_length, char input_length, char kind)
    cpdef size_t get_int(self) except ?ULLONG_MAX
    cpdef void set_int(self, size_t integer) except *
    cpdef list get_list(self)
    cpdef void set_list(self, list data) except *
    cpdef list list_get_and_set(self, list data)
    cpdef list list_compare_and_set_value(self, list i, list n)
    cpdef void reencode(self, str newencode) except *