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

from .enabled_13 import enabled as enabled_cls
from .ddpm_phase import ddpm_phase as ddpm_phase_cls
class volume_displacement(Group):
    """
    'volume_displacement' child.
    """

    fluent_name = "volume-displacement"

    child_names = \
        ['enabled', 'ddpm_phase']

    _child_classes = dict(
        enabled=enabled_cls,
        ddpm_phase=ddpm_phase_cls,
    )

