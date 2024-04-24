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

from .general_3 import general as general_cls
from .reference_frame_3 import reference_frame as reference_frame_cls
from .mesh_motion import mesh_motion as mesh_motion_cls
from .solid_motion import solid_motion as solid_motion_cls
from .sources import sources as sources_cls
from .fixed_values import fixed_values as fixed_values_cls
from .material_orientation import material_orientation as material_orientation_cls
from .disabled_1 import disabled as disabled_cls
from .internal import internal as internal_cls
class phase_child(Group):
    """
    'child_object_type' of phase.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['general', 'reference_frame', 'mesh_motion', 'solid_motion',
         'sources', 'fixed_values', 'material_orientation', 'disabled',
         'internal']

    _child_classes = dict(
        general=general_cls,
        reference_frame=reference_frame_cls,
        mesh_motion=mesh_motion_cls,
        solid_motion=solid_motion_cls,
        sources=sources_cls,
        fixed_values=fixed_values_cls,
        material_orientation=material_orientation_cls,
        disabled=disabled_cls,
        internal=internal_cls,
    )

