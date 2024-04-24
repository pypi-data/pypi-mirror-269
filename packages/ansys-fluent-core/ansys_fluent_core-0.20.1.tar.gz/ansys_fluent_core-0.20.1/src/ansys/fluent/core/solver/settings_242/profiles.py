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

from .display_profile_point_cloud_data import display_profile_point_cloud_data as display_profile_point_cloud_data_cls
from .display_profile_surface import display_profile_surface as display_profile_surface_cls
from .set_preference_profile_point_cloud_data import set_preference_profile_point_cloud_data as set_preference_profile_point_cloud_data_cls
from .overlay_profile_point_cloud_data import overlay_profile_point_cloud_data as overlay_profile_point_cloud_data_cls
from .overlay_profile_surface import overlay_profile_surface as overlay_profile_surface_cls
from .list_profiles import list_profiles as list_profiles_cls
from .list_profile_parameters import list_profile_parameters as list_profile_parameters_cls
from .list_profile_parameters_with_value import list_profile_parameters_with_value as list_profile_parameters_with_value_cls
from .list_profile_fields import list_profile_fields as list_profile_fields_cls
from .delete_4 import delete as delete_cls
from .delete_all_1 import delete_all as delete_all_cls
class profiles(Group):
    """
    Profile display menu.
    """

    fluent_name = "profiles"

    command_names = \
        ['display_profile_point_cloud_data', 'display_profile_surface',
         'set_preference_profile_point_cloud_data',
         'overlay_profile_point_cloud_data', 'overlay_profile_surface',
         'list_profiles', 'list_profile_parameters',
         'list_profile_parameters_with_value', 'list_profile_fields',
         'delete', 'delete_all']

    _child_classes = dict(
        display_profile_point_cloud_data=display_profile_point_cloud_data_cls,
        display_profile_surface=display_profile_surface_cls,
        set_preference_profile_point_cloud_data=set_preference_profile_point_cloud_data_cls,
        overlay_profile_point_cloud_data=overlay_profile_point_cloud_data_cls,
        overlay_profile_surface=overlay_profile_surface_cls,
        list_profiles=list_profiles_cls,
        list_profile_parameters=list_profile_parameters_cls,
        list_profile_parameters_with_value=list_profile_parameters_with_value_cls,
        list_profile_fields=list_profile_fields_cls,
        delete=delete_cls,
        delete_all=delete_all_cls,
    )

