import numpy
from .._types import ndarray_or_scalar
from exposedfunctionality import controlled_wrapper as wraps
import funcnodes as fn


@fn.NodeDecorator(
    node_id="np.emath.sqrt",
    name="sqrt",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.sqrt)
def sqrt(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.sqrt(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log",
    name="log",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log)
def log(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log2",
    name="log2",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log2)
def log2(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log2(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.logn",
    name="logn",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.logn)
def logn(
    n: int,
    x: ndarray_or_scalar,
):  # params ['n', 'x'] [] []
    res = numpy.emath.logn(
        n=n,
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.log10",
    name="log10",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.log10)
def log10(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.log10(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.power",
    name="power",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.power)
def power(
    x: ndarray_or_scalar,
    p: ndarray_or_scalar,
):  # params ['x', 'p'] [] []
    res = numpy.emath.power(
        x=x,
        p=p,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arccos",
    name="arccos",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arccos)
def arccos(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arccos(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arcsin",
    name="arcsin",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arcsin)
def arcsin(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arcsin(
        x=x,
    )
    return res


@fn.NodeDecorator(
    node_id="np.emath.arctanh",
    name="arctanh",
    outputs=[{"name": "out", "type": "ndarray_or_scalar"}],
)
@wraps(numpy.emath.arctanh)
def arctanh(
    x: ndarray_or_scalar,
):  # params ['x'] [] []
    res = numpy.emath.arctanh(
        x=x,
    )
    return res


NODE_SHELF = fn.Shelf(
    name="emath",
    nodes=[
        sqrt,
        log,
        log2,
        logn,
        log10,
        power,
        arccos,
        arcsin,
        arctanh,
    ],
    subshelves=[],
    description="emath functionalities for FuncNodes",
)
