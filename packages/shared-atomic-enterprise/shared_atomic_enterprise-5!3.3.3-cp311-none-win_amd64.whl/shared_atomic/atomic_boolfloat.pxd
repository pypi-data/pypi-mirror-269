from shared_atomic.atomic_object_backend cimport  atomic_object
from shared_atomic.atomic_object_backend cimport  subprocess_reference

cpdef bint bool_get(subprocess_reference reference) except *
cpdef void bool_set(subprocess_reference reference, bint n) except *
cpdef bint bool_get_and_set(subprocess_reference reference, bint n) except *
cpdef bint bool_compare_and_set_value(subprocess_reference reference, bint e, bint n) except *

cdef class atomic_bool(atomic_object):
    cpdef bint get(self) except *
    cpdef void set(self, bint value) except*
    cpdef bint bool_get_and_set(self, bint n) except *
    cpdef bint bool_compare_and_set_value(self, bint e, bint n) except *