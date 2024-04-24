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

from .observable_2 import observable as observable_cls
from .value_17 import value as value_cls
from .step_direction import step_direction as step_direction_cls
from .target_change import target_change as target_change_cls
from .change_as_percentage import change_as_percentage as change_as_percentage_cls
from .weight_3 import weight as weight_cls
class objectives_child(Group):
    """
    'child_object_type' of objectives.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['observable', 'value', 'step_direction', 'target_change',
         'change_as_percentage', 'weight']

    _child_classes = dict(
        observable=observable_cls,
        value=value_cls,
        step_direction=step_direction_cls,
        target_change=target_change_cls,
        change_as_percentage=change_as_percentage_cls,
        weight=weight_cls,
    )

