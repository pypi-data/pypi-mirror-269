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

from .profile_name_1 import profile_name as profile_name_cls
from .field_contour import field_contour as field_contour_cls
from .field_variable import field_variable as field_variable_cls
class display_profile_point_cloud_data(Command):
    """
    Display Profile Point cloud data Command.
    
    Parameters
    ----------
        profile_name : str
            Profile name.
        field_contour : bool
            Field contour?.
        field_variable : str
            Field variable.
    
    """

    fluent_name = "display-profile-point-cloud-data"

    argument_names = \
        ['profile_name', 'field_contour', 'field_variable']

    _child_classes = dict(
        profile_name=profile_name_cls,
        field_contour=field_contour_cls,
        field_variable=field_variable_cls,
    )

