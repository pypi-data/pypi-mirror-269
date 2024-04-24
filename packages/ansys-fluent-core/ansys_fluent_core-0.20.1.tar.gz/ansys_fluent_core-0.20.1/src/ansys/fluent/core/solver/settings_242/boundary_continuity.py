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

from .enabled_46 import enabled as enabled_cls
from .definition_2 import definition as definition_cls
from .continuity_order import continuity_order as continuity_order_cls
from .specify_boundary import specify_boundary as specify_boundary_cls
class boundary_continuity(Group):
    """
    Region boundary continuity conditions.
    """

    fluent_name = "boundary-continuity"

    child_names = \
        ['enabled', 'definition', 'continuity_order', 'specify_boundary']

    _child_classes = dict(
        enabled=enabled_cls,
        definition=definition_cls,
        continuity_order=continuity_order_cls,
        specify_boundary=specify_boundary_cls,
    )

