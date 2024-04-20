from shared_atomic.atomic_object_backend cimport subprocess_reference

from shared_atomic.atomic_object_backend cimport get_reference
from shared_atomic.atomic_object_backend cimport release_reference

from shared_atomic.atomic_int cimport int_get
from shared_atomic.atomic_int cimport int_set
from shared_atomic.atomic_int cimport int_get_and_set
from shared_atomic.atomic_int cimport int_compare_and_set_value
from shared_atomic.atomic_int cimport int_add_and_fetch
from shared_atomic.atomic_int cimport int_sub_and_fetch
from shared_atomic.atomic_int cimport int_fetch_and_add
from shared_atomic.atomic_int cimport int_fetch_and_sub
from shared_atomic.atomic_int cimport int_fetch_and_and
from shared_atomic.atomic_int cimport int_fetch_and_or
from shared_atomic.atomic_int cimport int_fetch_and_xor
from shared_atomic.atomic_int cimport int_bittest_and_set
from shared_atomic.atomic_int cimport int_bittest_and_reset
from shared_atomic.atomic_int cimport int_fetch_and_or

from shared_atomic.atomic_boolfloat cimport bool_get
from shared_atomic.atomic_boolfloat cimport bool_set
from shared_atomic.atomic_boolfloat cimport bool_get_and_set
from shared_atomic.atomic_boolfloat cimport bool_compare_and_set_value

from shared_atomic.atomic_bytearray cimport  array_get_int
from shared_atomic.atomic_bytearray cimport  array_get_bytes
from shared_atomic.atomic_bytearray cimport  array_set_bytes
from shared_atomic.atomic_bytearray cimport  array_get_and_set
from shared_atomic.atomic_bytearray cimport  array_compare_and_set_value
from shared_atomic.atomic_bytearray cimport  array_add_and_fetch
from shared_atomic.atomic_bytearray cimport  array_sub_and_fetch
from shared_atomic.atomic_bytearray cimport  array_fetch_and_add
from shared_atomic.atomic_bytearray cimport  array_fetch_and_sub
from shared_atomic.atomic_bytearray cimport  array_fetch_and_and
from shared_atomic.atomic_bytearray cimport  array_fetch_and_or
from shared_atomic.atomic_bytearray cimport  array_fetch_and_xor
from shared_atomic.atomic_bytearray cimport  array_bittest_and_set
from shared_atomic.atomic_bytearray cimport  array_bittest_and_reset

from shared_atomic.atomic_list cimport list_get_int
from shared_atomic.atomic_list cimport list_set_int
from shared_atomic.atomic_list cimport list_get_list
from shared_atomic.atomic_list cimport list_set_list
from shared_atomic.atomic_list cimport list_get_and_set
from shared_atomic.atomic_list cimport list_compare_and_set_value

from shared_atomic.atomic_set cimport set_get_int
from shared_atomic.atomic_set cimport set_set_int
from shared_atomic.atomic_set cimport set_get_set
from shared_atomic.atomic_set cimport set_set_set
from shared_atomic.atomic_set cimport set_get_and_set
from shared_atomic.atomic_set cimport set_compare_and_set_value

from shared_atomic.atomic_string cimport string_get_string
from shared_atomic.atomic_string cimport string_set_string
from shared_atomic.atomic_string cimport string_get_and_set
from shared_atomic.atomic_string cimport string_compare_and_set_value

from shared_atomic.atomic_shared_memory cimport shared_memory_offset_get
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_get_and_set
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_compare_and_set_value
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_add_and_fetch
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_sub_and_fetch
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_fetch_and_add
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_fetch_and_sub
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_fetch_and_and
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_fetch_and_or
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_fetch_and_xor

from shared_atomic.atomic_shared_memory cimport shared_memory_offset_bittest_and_set
from shared_atomic.atomic_shared_memory cimport shared_memory_offset_bittest_and_reset

from shared_atomic.atomic_object_backend cimport array2d