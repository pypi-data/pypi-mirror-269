import funcnodes as fn


from ._core import *


from ._lib import *
from ._linalg import *
from ._ndarray import *


from ._ndarray import NODE_SHELF as NODE_SHELF_ndarray
from ._linalg import NODE_SHELF as NODE_SHELF_linalg
from ._lib import EMATH_NODE_SHELF


from . import _core as core
from . import _linalg as linalg
from . import _ndarray as ndarray
from ._core._defchararray import NODE_SHELF as CHAR_NODE_SHELF
from .constants import NODE_SHELF as CONSTANTS_NODE_SHELF
from . import _types

from ._dtypes import DTYPE_ENUM

from exposedfunctionality.function_parser.types import type_to_string

import numpy as np

__version__ = "0.1.52"


# set the print options to display a smaller number of elements for node previews
np.set_printoptions(threshold=100)


def from_np(obj, preview=False):
    if isinstance(obj, np.ndarray):
        if preview:
            return str(obj), True
        else:
            return obj.tolist(), True

    return obj, False


fn.JSONEncoder.add_encoder(from_np)


FUNCNODES_RENDER_OPTIONS: fn.RenderOptions = {
    "typemap": {
        type_to_string(np.ndarray): "str",
    },
    "inputconverter": {
        type_to_string(np.ndarray): "str_to_list",
    },
}

ARRAY_CREATION_SHELF = fn.Shelf(
    name="Array Creation",
    description="Array Creation",
    nodes=[],
    subshelves=[
        fn.Shelf(
            name="Basic",
            description="Basic array creation",
            nodes=[
                core.arange,
                core.array,
                core.asarray,
                core.asanyarray,
                core.empty,
                core.empty_like,
                core.eye,
                core.full,
                core.full_like,
                core.identity,
                core.linspace,
                core.geomspace,
                core.logspace,
                core.ones,
                core.ones_like,
                core.zeros,
                core.zeros_like,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="From Existing Data",
            description="Array creation from existing data",
            nodes=[
                core.array,
                core.asarray,
                core.asanyarray,
                core.ascontiguousarray,
                core.asarray_chkfinite,
                core.asfarray,
                core.asfortranarray,
                core.asmatrix,
                core.copy,
                core.require,
                core.frombuffer,
                core.fromfunction,
                core.fromiter,
                core.fromstring,
                core.tile,
                core.repeat,
                core.diag,
                core.diagflat,
                core.broadcast_arrays,
                core.broadcast_to,
                core.copyto,
                core.mat,
                core.bmat,
                core.from_dlpack,
            ],
            subshelves=[],
        ),
    ],
)

MATH_OPERATIONS_SHELF = fn.Shelf(
    name="Mathematical Operations",
    description="Mathematical Operations",
    nodes=[],
    subshelves=[
        fn.Shelf(
            name="Arithmetic",
            description="Arithmetic",
            nodes=[
                core.add,
                core.subtract,
                core.multiply,
                core.divide,
                core.true_divide,
                core.floor_divide,
                core.mod,
                core.power,
                core.remainder,
                core.reciprocal,
                core.divmod,
                core.cumsum,
                core.cumprod,
                core.nancumsum,
                core.nancumprod,
                core.nansum,
                core.nanprod,
                core.square,
                core.positive,
                core.negative,
                core.float_power,
                core.lcm,
                core.gcd,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Rounding",
            description="Rounding",
            nodes=[
                core.round,
                core.fix,
                core.floor,
                core.ceil,
                core.trunc,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Trigonometric",
            description="Trigonometric",
            nodes=[
                core.sin,
                core.cos,
                core.tan,
                core.arcsin,
                core.arccos,
                core.arctan,
                core.arctan2,
                core.hypot,
                core.degrees,
                core.radians,
                core.deg2rad,
                core.rad2deg,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Hyperbolic",
            description="Hyperbolic",
            nodes=[
                core.sinh,
                core.cosh,
                core.tanh,
                core.arcsinh,
                core.arccosh,
                core.arctanh,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Exponential and Logarithmic",
            description="Exponential and Logarithmic",
            nodes=[
                core.exp,
                core.exp2,
                core.log,
                core.log10,
                core.log2,
                core.log1p,
                core.expm1,
                core.logaddexp,
                core.logaddexp2,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Complex Numbers",
            description="Complex Numbers",
            nodes=[
                core.angle,
                core.conj,
                core.conjugate,
                core.imag,
                core.real,
                core.iscomplex,
                core.isreal,
                core.isrealobj,
                core.iscomplexobj,
                core.real_if_close,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Special Functions",
            description="Special Functions",
            nodes=[core.i0, core.sinc, core.unwrap, core.heaviside],
            subshelves=[],
        ),
        fn.Shelf(
            name="Miscellaneous",
            description="Miscellaneous",
            nodes=[
                core.absolute,
                core.cbrt,
                core.ceil,
                core.copysign,
                core.fabs,
                core.floor,
                core.fmod,
                core.frexp,
                core.ldexp,
                core.modf,
                core.nextafter,
                core.rint,
                core.sign,
                core.signbit,
                core.trunc,
                core.convolve,
            ],
            subshelves=[],
        ),
    ],
)

STATISTICAL_OPERATIONS_SHELF = fn.Shelf(
    name="Statistical Operations",
    description="Statistical Operations",
    nodes=[
        core.average,
        core.bincount,
        core.corrcoef,
        core.cov,
        core.correlate,
        core.histogram,
        core.histogram2d,
        core.histogramdd,
        core.histogramdd,
        core.histogram_bin_edges,
        core.mean,
        core.nanmean,
        core.median,
        core.nanmedian,
        core.std,
        core.nanstd,
        core.var,
        core.nanvar,
        core.max,
        core.nanmax,
        core.fmax,
        core.min,
        core.fmin,
        core.nanmin,
        core.ptp,
        core.percentile,
        core.nanpercentile,
        core.quantile,
        core.nanquantile,
        core.minimum,
        core.maximum,
        ndarray.argmax,
        ndarray.argmin,
    ],
    subshelves=[],
)

ARRAY_MANIPULATION_SHELF = fn.Shelf(
    name="Array Manipulation",
    description="Array Manipulation",
    nodes=[],
    subshelves=[
        fn.Shelf(
            name="Basic Operations",
            description="Basic Operations",
            nodes=[
                core.reshape,
                core.ravel,
                ndarray.flatten,
                core.expand_dims,
                core.squeeze,
                core.transpose,
                core.swapaxes,
                core.nan_to_num,
                core.rollaxis,
                core.moveaxis,
                core.resize,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Changing Number of Dimensions",
            description="Changing Number of Dimensions",
            nodes=[core.atleast_1d, core.atleast_2d, core.atleast_3d],
            subshelves=[],
        ),
        fn.Shelf(
            name="Joining and Splitting",
            description="Joining and Splitting",
            nodes=[
                core.concatenate,
                core.stack,
                core.vstack,
                core.hstack,
                core.dstack,
                core.column_stack,
                core.row_stack,
                core.split,
                core.array_split,
                core.dsplit,
                core.hsplit,
                core.vsplit,
            ],
            subshelves=[],
        ),
        fn.Shelf(
            name="Adding and Removing Elements",
            description="Adding and Removing Elements",
            nodes=[core.append, core.delete, core.insert, core.pad],
            subshelves=[],
        ),
        fn.Shelf(
            name="Rearranging Elements",
            description="Rearranging Elements",
            nodes=[
                core.flip,
                core.fliplr,
                core.flipud,
                core.roll,
                core.rot90,
                core.trim_zeros,
            ],
            subshelves=[],
        ),
    ],
)

LOGIGAL_OPERATIONS_SHELF = fn.Shelf(
    name="Logical Operations",
    description="Logical Operations",
    nodes=[
        core.all,
        core.any,
        core.allclose,
        core.isclose,
        core.array_equal,
        core.array_equiv,
        core.greater,
        core.greater_equal,
        core.less,
        core.less_equal,
        core.not_equal,
        core.equal,
        core.logical_and,
        core.logical_or,
        core.logical_not,
        core.logical_xor,
        core.isfinite,
        core.isinf,
        core.isneginf,
        core.isposinf,
        core.isnan,
    ],
    subshelves=[],
)

BITWISE_OPERATIONS_SHELF = fn.Shelf(
    name="Bitwise Operations",
    description="Bitwise Operations",
    nodes=[
        core.bitwise_and,
        core.bitwise_or,
        core.bitwise_xor,
        core.invert,
        core.left_shift,
        core.right_shift,
        core.packbits,
    ],
    subshelves=[],
)


MISC_UTILITIES_SHELF = fn.Shelf(
    name="Miscellaneous Utilities",
    description="Miscellaneous Utilities",
    nodes=[
        core.clip,
        core.cross,
        core.cumprod,
        core.cumsum,
        core.diff,
        core.ediff1d,
        core.gradient,
        core.interp,
        core.meshgrid,
        core.percentile,
        core.quantile,
        core.trapz,
        core.tri,
        core.tril,
        core.triu,
        core.unique,
        core.unpackbits,
        core.vander,
        core.where,
        core.shape,
        core.size,
        core.ndim,
        core.isscalar,
        core.digitize,
        core.spacing,
        core.binary_repr,
        core.isfortran,
    ],
    subshelves=[],
)

DECOMPOSITION_SHELF = fn.Shelf(
    name="Decomposition",
    description="Decomposition",
    nodes=[
        linalg.qr,
        linalg.svd,
        linalg.cholesky,
        linalg.eig,
        linalg.eigh,
        linalg.eigvals,
        linalg.eigvalsh,
    ],
    subshelves=[],
)

LINEAR_ALGEBRA_SHELF = fn.Shelf(
    name="Linear Algebra",
    description="Linear Algebra",
    nodes=[
        core.dot,
        core.vdot,
        core.inner,
        core.outer,
        core.matmul,
        core.tensordot,
        core.kron,
        core.einsum,
        core.einsum_path,
        linalg.solve,
        linalg.tensorinv,
        linalg.tensorsolve,
        linalg.det,
        linalg.slogdet,
        linalg.inv,
        linalg.pinv,
        linalg.qr,
        linalg.svd,
        linalg.cholesky,
        linalg.eig,
        linalg.eigh,
        linalg.eigvals,
        linalg.eigvalsh,
        linalg.lstsq,
    ],
    subshelves=[],
)

MATRIX_OPERATIONS_SHELF = fn.Shelf(
    name="Matrix Operations",
    description="Matrix Operations",
    nodes=[
        core.matmul,
        linalg.matrix_power,
    ],
    subshelves=[],
)

DATETIME_SHELF = fn.Shelf(
    name="Datetime",
    description="Datetime",
    nodes=[
        core.datetime64,
        core.isnat,
    ],
    subshelves=[],
)

NODE_SHELF = fn.Shelf(
    name="numpy",
    nodes=[],
    subshelves=[
        ARRAY_CREATION_SHELF,
        CONSTANTS_NODE_SHELF,
        MATH_OPERATIONS_SHELF,
        STATISTICAL_OPERATIONS_SHELF,
        ARRAY_MANIPULATION_SHELF,
        LOGIGAL_OPERATIONS_SHELF,
        BITWISE_OPERATIONS_SHELF,
        MISC_UTILITIES_SHELF,
        DECOMPOSITION_SHELF,
        LINEAR_ALGEBRA_SHELF,
        MATRIX_OPERATIONS_SHELF,
        CHAR_NODE_SHELF,
        NODE_SHELF_ndarray,
        NODE_SHELF_linalg,
        EMATH_NODE_SHELF,
        DATETIME_SHELF,
    ],
    description="numpy functionalities for FuncNodes",
)
