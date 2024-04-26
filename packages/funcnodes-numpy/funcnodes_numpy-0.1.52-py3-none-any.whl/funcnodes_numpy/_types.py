import numpy
from typing import List, Union, Literal, Callable
from typing import TYPE_CHECKING

import exposedfunctionality.function_parser.types as exf_types

scalar = Union[int, float]
exf_types.add_type(Union[int, float], "scalar")
# exf_types.add_type(scalar, "scalar")
number = Union[complex, int, float]
exf_types.add_type(Union[complex, int, float], "number")
basic_types = Union[int, float, complex, str, bool]
exf_types.add_type(Union[int, float, complex, str, bool], "basic_types")
# exf_types.add_type(number, "number")

ndarray_or_scalar = Union[numpy.ndarray, scalar]
exf_types.add_type(Union[numpy.ndarray, scalar], "ndarray_or_scalar")
# exf_types.add_type(ndarray_or_scalar, "ndarray_or_scalar")

ndarray_or_number = Union[numpy.ndarray, number]
# exf_types.add_type(Union[numpy.ndarray, number], "ndarray_or_number")
exf_types.add_type(ndarray_or_number, "ndarray_or_number")

indices_or_sections = Union[int, List[int]]
# exf_types.add_type(Union[int, List[int]], "indices_or_sections")
exf_types.add_type(indices_or_sections, "indices_or_sections")

ndarray = numpy.ndarray
exf_types.add_type(numpy.ndarray, "ndarray")

shape_like = Union[ndarray, int, List[int]]
exf_types.add_type(Union[ndarray, int, List[int]], "shape_like")

axis_like = Union[int, List[int]]
exf_types.add_type(Union[int, List[int]], "axis_like")


array_like = Union[numpy.ndarray, basic_types]
exf_types.add_type(Union[numpy.ndarray, basic_types], "array_like")

int_array = ndarray
exf_types.add_type(ndarray, "int_array")

bool_array = ndarray
exf_types.add_type(ndarray, "bool_array")

bitarray = ndarray  # uint8
exf_types.add_type(ndarray, "bitarray")

bool_or_bool_array = Union[bool, bool_array]
exf_types.add_type(Union[bool, bool_array], "bool_or_bool_array")
# exf_types.add_type(bool_or_bool_array, "bool_or_bool_array")

int_bool_array = Union[int_array, bool_array]
exf_types.add_type(Union[int_array, bool_array], "int_bool_array")
# exf_types.add_type(int_bool_array, "int_bool_array")

int_or_int_array = Union[int, int_array]
exf_types.add_type(Union[int, int_array], "int_or_int_array")
##exf_types.add_type(int_or_int_array, "int_or_int_array")

real_array = ndarray
exf_types.add_type(ndarray, "real_array")

matrix = ndarray
exf_types.add_type(ndarray, "matrix")

OrderCF = Literal[None, "C", "F"]
exf_types.add_type(Literal[None, "C", "F"], "OrderCF")
# exf_types.add_type(OrderCF, "OrderCF")

OrderKACF = Literal[None, "K", "A", "C", "F"]
exf_types.add_type(Literal[None, "K", "A", "C", "F"], "OrderKACF")
# exf_types.add_type(OrderKACF, "OrderKACF")

OrderACF = Literal[None, "A", "C", "F"]
exf_types.add_type(Literal[None, "A", "C", "F"], "OrderACF")
# exf_types.add_type(OrderACF, "OrderACF")

buffer_like = Union[bytes, bytearray, memoryview, ndarray]
exf_types.add_type(Union[bytes, bytearray, memoryview, ndarray], "buffer_like")
# exf_types.add_type(buffer_like, "buffer_like")

if TYPE_CHECKING:
    str_array = numpy._ArrayLikeStr_co
    exf_types.add_type(numpy._ArrayLikeStr_co, "str_array")
else:
    str_array = numpy._typing._ArrayLikeStr_co
    exf_types.add_type(numpy._typing._ArrayLikeStr_co, "str_array")
##exf_types.add_type(str_array, "str_array")

UNSET = object()
NoValue = numpy._NoValue
exf_types.add_type(numpy._NoValue, "<no value>")
UnKnOWn = object()
casting_literal = Literal["no", "equiv", "safe", "same_kind", "unsafe"]
exf_types.add_type(
    Literal["no", "equiv", "safe", "same_kind", "unsafe"], "casting_literal"
)
# exf_types.add_type(casting_literal, "casting_literal")


Ufunc = Callable
exf_types.add_type(Callable, "Ufunc")
