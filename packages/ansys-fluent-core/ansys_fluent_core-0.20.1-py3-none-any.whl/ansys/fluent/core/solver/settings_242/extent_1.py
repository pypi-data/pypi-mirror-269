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

from .theta_3 import theta as theta_cls
from .radial_2 import radial as radial_cls
from .axial_1 import axial as axial_cls
class extent(Group):
    """
    Cylindrical design region extents.
    """

    fluent_name = "extent"

    child_names = \
        ['theta', 'radial', 'axial']

    _child_classes = dict(
        theta=theta_cls,
        radial=radial_cls,
        axial=axial_cls,
    )

