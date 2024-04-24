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

from .min_cell_volume import min_cell_volume as min_cell_volume_cls
from .min_orthogonal import min_orthogonal as min_orthogonal_cls
from .print_current_status import print_current_status as print_current_status_cls
class criteria(Group):
    """
    Mesh quality settings.
    """

    fluent_name = "criteria"

    child_names = \
        ['min_cell_volume', 'min_orthogonal']

    command_names = \
        ['print_current_status']

    _child_classes = dict(
        min_cell_volume=min_cell_volume_cls,
        min_orthogonal=min_orthogonal_cls,
        print_current_status=print_current_status_cls,
    )

