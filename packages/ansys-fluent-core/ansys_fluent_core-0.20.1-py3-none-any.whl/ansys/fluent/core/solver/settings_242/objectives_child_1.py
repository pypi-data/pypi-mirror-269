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

from .id_2 import id as id_cls
from .condition_1 import condition as condition_cls
from .observable_3 import observable as observable_cls
from .goal import goal as goal_cls
from .step_size_1 import step_size as step_size_cls
from .as_percentage import as_percentage as as_percentage_cls
class objectives_child(Group):
    """
    'child_object_type' of objectives.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['id', 'condition', 'observable', 'goal', 'step_size',
         'as_percentage']

    _child_classes = dict(
        id=id_cls,
        condition=condition_cls,
        observable=observable_cls,
        goal=goal_cls,
        step_size=step_size_cls,
        as_percentage=as_percentage_cls,
    )

