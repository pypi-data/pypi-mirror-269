import numpy
from typing import Optional, TYPE_CHECKING
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn

from .._types import str_array


@fn.NodeDecorator(
    node_id="np.char.array",
    name="array",
    outputs=[],
)
@wraps(numpy.char.array)
def chararray(
    obj: str_array,
    itemsize: Optional[int] = None,
    # copy: bool = True,
    # unicode: Optional[bool] = None,
    # order: OrderACF = None,
):  # params ['obj'] ['itemsize'] []
    res = numpy.char.array(
        obj,
        itemsize,
        # copy=copy,
        # unicode=unicode,
        # order=order
    )
    return res


@fn.NodeDecorator(
    node_id="np.char.asarray",
    name="asarray",
    outputs=[],
)
@wraps(numpy.char.asarray)
def aschararray(
    obj: str_array,
    itemsize: Optional[int],
    # unicode: Optional[bool] = None,
    # order: OrderCF = None,
):  # params ['obj'] ['itemsize'] []
    res = numpy.char.asarray(
        obj,
        itemsize,
        # unicode=unicode,
        # order=order
    )
    return res


NODE_SHELF = fn.Shelf(
    name="char arrays",
    description="char",
    nodes=[chararray, aschararray],
    subshelves=[],
)
