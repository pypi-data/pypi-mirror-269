from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport  subprocess_reference
from libc.limits cimport LLONG_MAX

cpdef long long int_get(subprocess_reference reference) except? LLONG_MAX
cpdef void int_set(subprocess_reference reference, long long n) except *
cpdef long long int_get_and_set(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_compare_and_set_value(subprocess_reference reference, long long e, long long n) except? LLONG_MAX
cpdef long long int_add_and_fetch(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_sub_and_fetch(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_fetch_and_add(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_fetch_and_sub(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_fetch_and_and(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_fetch_and_or(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_fetch_and_xor(subprocess_reference reference, long long n) except? LLONG_MAX
cpdef long long int_bittest_and_set(subprocess_reference reference, long long offset) except 2
cpdef unsigned char int_bittest_and_reset(subprocess_reference reference, long long offset) except 2

cdef class atomic_int(atomic_object):

    cpdef long long get(self) except ?LLONG_MAX
    cpdef void set(self, long long value) except *
    cpdef long long int_get_and_set(self, long long n) except ?LLONG_MAX
    cpdef long long int_compare_and_set_value(self, long long e, long long n) except ?LLONG_MAX
    cpdef long long int_add_and_fetch(self, long long n) except ?LLONG_MAX
    cpdef long long int_sub_and_fetch(self, long long n) except ?LLONG_MAX
    cpdef long long int_fetch_and_add(self, long long n) except ?LLONG_MAX
    cpdef long long int_fetch_and_sub(self, long long n) except ?LLONG_MAX
    cpdef long long int_fetch_and_and(self, long long n) except ?LLONG_MAX
    cpdef long long int_fetch_and_or(self, long long n) except ?LLONG_MAX
    cpdef long long int_fetch_and_xor(self, long long n) except ?LLONG_MAX
    cpdef long long int_bittest_and_set(self, long long offset) except ?LLONG_MAX
    cpdef long long int_bittest_and_reset(self, long long offset) except ?LLONG_MAX
