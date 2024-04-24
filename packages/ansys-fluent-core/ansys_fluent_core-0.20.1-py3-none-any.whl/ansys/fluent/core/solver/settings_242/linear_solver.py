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

from .tolerance_5 import tolerance as tolerance_cls
from .max_subiteration import max_subiteration as max_subiteration_cls
from .number_of_modes_1 import number_of_modes as number_of_modes_cls
class linear_solver(Group):
    """
    RBF linear solver settings menu.
    """

    fluent_name = "linear-solver"

    child_names = \
        ['tolerance', 'max_subiteration', 'number_of_modes']

    _child_classes = dict(
        tolerance=tolerance_cls,
        max_subiteration=max_subiteration_cls,
        number_of_modes=number_of_modes_cls,
    )

