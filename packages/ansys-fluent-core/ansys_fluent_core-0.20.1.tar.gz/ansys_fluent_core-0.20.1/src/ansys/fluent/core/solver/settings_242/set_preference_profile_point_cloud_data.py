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

from .profile_point_marker import profile_point_marker as profile_point_marker_cls
from .profile_point_marker_size import profile_point_marker_size as profile_point_marker_size_cls
from .profile_point_marker_color import profile_point_marker_color as profile_point_marker_color_cls
class set_preference_profile_point_cloud_data(Command):
    """
    Profile Point attributes command.
    
    Parameters
    ----------
        profile_point_marker : str
            Profile point marker.
        profile_point_marker_size : real
            Profile point marker size.
        profile_point_marker_color : str
            Profile point marker color.
    
    """

    fluent_name = "set-preference-profile-point-cloud-data"

    argument_names = \
        ['profile_point_marker', 'profile_point_marker_size',
         'profile_point_marker_color']

    _child_classes = dict(
        profile_point_marker=profile_point_marker_cls,
        profile_point_marker_size=profile_point_marker_size_cls,
        profile_point_marker_color=profile_point_marker_color_cls,
    )

