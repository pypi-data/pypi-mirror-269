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
class list_profile_parameters(Command):
    """
    List-profile-parameters-command.
    
    Parameters
    ----------
        profile_name : str
            Profile name.
    
    """

    fluent_name = "list-profile-parameters"

    argument_names = \
        ['profile_name']

    _child_classes = dict(
        profile_name=profile_name_cls,
    )

