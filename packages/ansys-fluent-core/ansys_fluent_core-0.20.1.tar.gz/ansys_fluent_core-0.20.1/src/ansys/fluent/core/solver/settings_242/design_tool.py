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

from .morpher import morpher as morpher_cls
from .region import region as region_cls
from .design_conditions import design_conditions as design_conditions_cls
from .objectives_1 import objectives as objectives_cls
from .design_change import design_change as design_change_cls
class design_tool(Group):
    """
    Gradient-based design tool menu.
    """

    fluent_name = "design-tool"

    child_names = \
        ['morpher', 'region', 'design_conditions', 'objectives',
         'design_change']

    _child_classes = dict(
        morpher=morpher_cls,
        region=region_cls,
        design_conditions=design_conditions_cls,
        objectives=objectives_cls,
        design_change=design_change_cls,
    )

