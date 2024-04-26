from typing import Optional, Union
import numpy
from .._types import ndarray
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn


@fn.NodeDecorator(
    node_id="np.datetime64",
    name="datetime64",
    outputs=[{"name": "date", "type": "ndarray"}],
)
@wraps(numpy.datetime64)
def datetime64(
    date: Union[str, int, ndarray],
    unit: Optional[str] = None,
):
    res = numpy.datetime64(
        date,
        unit=unit,
    )
    return res
