from libc.limits cimport ULLONG_MAX
from shared_atomic.atomic_object_backend cimport atomic_object
from shared_atomic.atomic_object_backend cimport subprocess_reference

cpdef bytes shared_memory_offset_get(atomic_shared_memory memory, subprocess_reference reference, long long offset = *, char length = *)
cpdef bytes shared_memory_offset_get_and_set(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset  = *)
cpdef bytes shared_memory_offset_compare_and_set_value(atomic_shared_memory memory, subprocess_reference reference, bytes i, bytes n, size_t offset=*)
cpdef bytes shared_memory_offset_add_and_fetch(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_sub_and_fetch(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_fetch_and_add(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_fetch_and_sub(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_fetch_and_and(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_fetch_and_or(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)
cpdef bytes shared_memory_offset_fetch_and_xor(atomic_shared_memory memory, subprocess_reference reference, bytes value, size_t offset = *)

cpdef bint shared_memory_offset_bittest_and_set(atomic_shared_memory memory, subprocess_reference reference, size_t left_offset = *) except *
cpdef bint shared_memory_offset_bittest_and_reset(atomic_shared_memory memory, subprocess_reference reference, size_t left_offset = *) except *

cdef class atomic_shared_memory(atomic_object):
    cdef readonly bint x13
    cdef long long x14
    cdef public bint x15
    cdef str x16
    cdef Py_ssize_t x18[1]
    cdef Py_ssize_t x19[1]
    cdef size_t x20

    cdef bytes s6(self, str previous_shared_memory_path)
    cdef list s7(self, size_t length)
    cdef int s8(self) except -1
    cpdef void y2(self,
                                            object_id: int,
                                            bint windows_unix_compatibility,
                                            long long reference_m,
                                            size_t size,
                                            int creation_pid,
                                            size_t total_size_including_ending_zeros=*) except*

    cpdef int file_sync(self, bint async=*, size_t start=*, size_t length=*) except -1
    cdef int s2(self, char operation_length) except -1

    cpdef void offset_memmove(self, mv:memoryview, size_t offset = *, str io_flags = *) except *
    cpdef bytes offset_get(self, size_t offset  = *, char length = *)
    cpdef bytes offset_get_and_set(self, bytes value, size_t offset  = *)
    cpdef bytes offset_compare_and_set_value(self, bytes i, bytes n, size_t offset  = *)

    cpdef bytes offset_add_and_fetch(self, bytes value, size_t offset  = *)
    cpdef bytes  offset_sub_and_fetch(self, bytes value, size_t offset  = *)

    cpdef bytes offset_fetch_and_add(self, bytes value, size_t offset=*)
    cpdef bytes offset_fetch_and_sub(self, bytes value, size_t offset=*)
    cpdef bytes offset_fetch_and_and(self, bytes value, size_t offset=*)
    cpdef bytes offset_fetch_and_or(self, bytes value, size_t offset=*)
    cpdef bytes offset_fetch_and_xor(self, bytes value, size_t offset=*)

    cpdef bint offset_bittest_and_set(self, size_t left_offset) except *
    cpdef bint offset_bittest_and_reset(self, size_t left_offset) except*


    cpdef char [: , ::1] offset_gets(self, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_get_and_sets(self, const char[:,:]  values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_compare_and_set_values(self, const char[:,:] ies, const char[:,:] ns, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *

    cpdef char [: , ::1] offset_add_and_fetches(self, const char[:,:] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_sub_and_fetches(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *

    cpdef char [: , ::1] offset_fetch_and_adds(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_fetch_and_subs(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_fetch_and_ands(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_fetch_and_ors(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *
    cpdef char [: , ::1] offset_fetch_and_xors(self, const char[:, :] values, const size_t[:] offsets, const char[:] lengths, size_t parallelism=*) except *

    cpdef unsigned char [::1] offset_bittest_and_sets(self, const size_t[:] left_offsets, size_t parallelism=*) except *
    cpdef unsigned char [::1] offset_bittest_and_resets(self, const size_t[:] left_offsets, size_t parallelism=*) except *

    cdef void s3(self,  unsigned char[:] mv, unsigned char * reference, size_t length) except *
    cdef void s4(self,  const unsigned char[:] mv, unsigned char * reference, size_t length) except *
    cpdef void offset_memmove(self, mv: memoryview, size_t offset = *, str io_flags =*) except *
    cpdef size_t memdump(self, str file_path, size_t start=*, size_t length=*) except ?ULLONG_MAX
    cdef tuple s5(self, size_t start, size_t length)








