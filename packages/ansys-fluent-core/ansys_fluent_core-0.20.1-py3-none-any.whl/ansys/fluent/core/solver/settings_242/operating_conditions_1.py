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

from .count_1 import count as count_cls
from .parameters_count import parameters_count as parameters_count_cls
from .parameters_5 import parameters as parameters_cls
from .conditions_2 import conditions as conditions_cls
class operating_conditions(Group):
    """
    Operating conditions for multiobjective optimization.
    """

    fluent_name = "operating-conditions"

    child_names = \
        ['count', 'parameters_count', 'parameters', 'conditions']

    _child_classes = dict(
        count=count_cls,
        parameters_count=parameters_count_cls,
        parameters=parameters_cls,
        conditions=conditions_cls,
    )

