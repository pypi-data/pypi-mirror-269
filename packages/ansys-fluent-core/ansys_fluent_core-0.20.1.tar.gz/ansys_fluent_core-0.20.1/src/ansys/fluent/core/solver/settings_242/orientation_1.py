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

from .skip_3 import skip as skip_cls
from .reverse_surfaces import reverse_surfaces as reverse_surfaces_cls
class orientation(Group):
    """
    Orientation to ensure that surfaces are constrained on the correct side of the Imported Surfaces (that is, the side that has a positive orientation).
    """

    fluent_name = "orientation"

    child_names = \
        ['skip']

    command_names = \
        ['reverse_surfaces']

    _child_classes = dict(
        skip=skip_cls,
        reverse_surfaces=reverse_surfaces_cls,
    )

