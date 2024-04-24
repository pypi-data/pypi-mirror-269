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

from .second_order import second_order as second_order_cls
from .increase_local_smoothness import increase_local_smoothness as increase_local_smoothness_cls
from .increase_global_smoothness import increase_global_smoothness as increase_global_smoothness_cls
from .tolerance_4 import tolerance as tolerance_cls
class constraint_settings(Group):
    """
    Constraint settings.
    """

    fluent_name = "constraint-settings"

    child_names = \
        ['second_order', 'increase_local_smoothness',
         'increase_global_smoothness', 'tolerance']

    _child_classes = dict(
        second_order=second_order_cls,
        increase_local_smoothness=increase_local_smoothness_cls,
        increase_global_smoothness=increase_global_smoothness_cls,
        tolerance=tolerance_cls,
    )

