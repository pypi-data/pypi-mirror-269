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

from .id_1 import id as id_cls
from .active_2 import active as active_cls
from .parameters_6 import parameters as parameters_cls
class conditions_child(Group):
    """
    'child_object_type' of conditions.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['id', 'active', 'parameters']

    _child_classes = dict(
        id=id_cls,
        active=active_cls,
        parameters=parameters_cls,
    )

