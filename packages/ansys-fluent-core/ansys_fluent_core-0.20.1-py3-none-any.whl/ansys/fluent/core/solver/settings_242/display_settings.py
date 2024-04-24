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

from .auto_display_1 import auto_display as auto_display_cls
from .schematic import schematic as schematic_cls
from .constrained_nodes import constrained_nodes as constrained_nodes_cls
from .surfaces_inside_region_only import surfaces_inside_region_only as surfaces_inside_region_only_cls
class display_settings(Group):
    """
    Display options menu.
    """

    fluent_name = "display-settings"

    child_names = \
        ['auto_display', 'schematic', 'constrained_nodes',
         'surfaces_inside_region_only']

    _child_classes = dict(
        auto_display=auto_display_cls,
        schematic=schematic_cls,
        constrained_nodes=constrained_nodes_cls,
        surfaces_inside_region_only=surfaces_inside_region_only_cls,
    )

