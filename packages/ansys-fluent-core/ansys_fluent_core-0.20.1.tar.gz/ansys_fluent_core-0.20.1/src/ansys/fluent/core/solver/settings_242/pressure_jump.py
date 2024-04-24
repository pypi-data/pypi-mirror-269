#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .option_18 import option as option_cls
from .function_of import function_of as function_of_cls
from .value_13 import value as value_cls
from .udf_1 import udf as udf_cls
from .piecewise_polynomial import piecewise_polynomial as piecewise_polynomial_cls
from .piecewise_linear_2 import piecewise_linear as piecewise_linear_cls
from .polynomial_2 import polynomial as polynomial_cls
class pressure_jump(Group):
    """
    Pressure Jump.
    """

    fluent_name = "pressure-jump"

    child_names = \
        ['option', 'function_of', 'value', 'udf', 'piecewise_polynomial',
         'piecewise_linear', 'polynomial']

    _child_classes = dict(
        option=option_cls,
        function_of=function_of_cls,
        value=value_cls,
        udf=udf_cls,
        piecewise_polynomial=piecewise_polynomial_cls,
        piecewise_linear=piecewise_linear_cls,
        polynomial=polynomial_cls,
    )

