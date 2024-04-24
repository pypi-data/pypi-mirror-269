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

from .in_plane_motion_only import in_plane_motion_only as in_plane_motion_only_cls
from .x_motion import x_motion as x_motion_cls
from .x_continuity import x_continuity as x_continuity_cls
from .y_motion import y_motion as y_motion_cls
from .y_continuity import y_continuity as y_continuity_cls
from .z_motion import z_motion as z_motion_cls
from .z_continuity import z_continuity as z_continuity_cls
from .theta_motion import theta_motion as theta_motion_cls
from .theta_continuity import theta_continuity as theta_continuity_cls
from .radial_motion import radial_motion as radial_motion_cls
from .radial_continuity import radial_continuity as radial_continuity_cls
from .axial_motion import axial_motion as axial_motion_cls
from .axial_continuity import axial_continuity as axial_continuity_cls
class specify_boundary_child(Group):
    """
    'child_object_type' of specify_boundary.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['in_plane_motion_only', 'x_motion', 'x_continuity', 'y_motion',
         'y_continuity', 'z_motion', 'z_continuity', 'theta_motion',
         'theta_continuity', 'radial_motion', 'radial_continuity',
         'axial_motion', 'axial_continuity']

    _child_classes = dict(
        in_plane_motion_only=in_plane_motion_only_cls,
        x_motion=x_motion_cls,
        x_continuity=x_continuity_cls,
        y_motion=y_motion_cls,
        y_continuity=y_continuity_cls,
        z_motion=z_motion_cls,
        z_continuity=z_continuity_cls,
        theta_motion=theta_motion_cls,
        theta_continuity=theta_continuity_cls,
        radial_motion=radial_motion_cls,
        radial_continuity=radial_continuity_cls,
        axial_motion=axial_motion_cls,
        axial_continuity=axial_continuity_cls,
    )

