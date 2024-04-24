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

from .name import name as name_cls
from .phase_5 import phase as phase_cls
from .pressure_jump_specification import pressure_jump_specification as pressure_jump_specification_cls
from .swirl_velocity_specification import swirl_velocity_specification as swirl_velocity_specification_cls
from .geometry_3 import geometry as geometry_cls
from .adjacent_cell_zone import adjacent_cell_zone as adjacent_cell_zone_cls
from .shadow_face_zone import shadow_face_zone as shadow_face_zone_cls
class fan_child(Group):
    """
    'child_object_type' of fan.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['name', 'phase', 'pressure_jump_specification',
         'swirl_velocity_specification', 'geometry']

    query_names = \
        ['adjacent_cell_zone', 'shadow_face_zone']

    _child_classes = dict(
        name=name_cls,
        phase=phase_cls,
        pressure_jump_specification=pressure_jump_specification_cls,
        swirl_velocity_specification=swirl_velocity_specification_cls,
        geometry=geometry_cls,
        adjacent_cell_zone=adjacent_cell_zone_cls,
        shadow_face_zone=shadow_face_zone_cls,
    )

