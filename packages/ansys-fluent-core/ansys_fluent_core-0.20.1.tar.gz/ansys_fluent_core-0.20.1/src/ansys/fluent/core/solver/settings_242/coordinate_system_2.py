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

from .origin_3 import origin as origin_cls
from .axis_4 import axis as axis_cls
from .radial_1 import radial as radial_cls
class coordinate_system(Group):
    """
    Design tool cylindrical frame of reference menu.
    """

    fluent_name = "coordinate-system"

    child_names = \
        ['origin', 'axis', 'radial']

    _child_classes = dict(
        origin=origin_cls,
        axis=axis_cls,
        radial=radial_cls,
    )

