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

from .value_18 import value as value_cls
from .affected_conditions import affected_conditions as affected_conditions_cls
class parameters_child(Group):
    """
    'child_object_type' of parameters.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['value', 'affected_conditions']

    _child_classes = dict(
        value=value_cls,
        affected_conditions=affected_conditions_cls,
    )

