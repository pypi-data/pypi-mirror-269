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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .invariant_expert_controls_child import invariant_expert_controls_child

class invariant_expert_controls(ListObject[invariant_expert_controls_child]):
    """
    Advanced settings for invariant motion.
    """

    fluent_name = "invariant-expert-controls"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: invariant_expert_controls_child = invariant_expert_controls_child
    """
    child_object_type of invariant_expert_controls.
    """
