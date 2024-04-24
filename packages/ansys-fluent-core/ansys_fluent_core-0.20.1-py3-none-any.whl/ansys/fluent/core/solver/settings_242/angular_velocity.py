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

from .x_4 import x as x_cls
from .x_2_1 import x_2 as x_2_cls
from .y_4 import y as y_cls
from .y_2_1 import y_2 as y_2_cls
from .z_4 import z as z_cls
from .z_2_1 import z_2 as z_2_cls
from .magnitude_1 import magnitude as magnitude_cls
class angular_velocity(Group):
    """
    'angular_velocity' child.
    """

    fluent_name = "angular-velocity"

    child_names = \
        ['x', 'x_2', 'y', 'y_2', 'z', 'z_2', 'magnitude']

    _child_classes = dict(
        x=x_cls,
        x_2=x_2_cls,
        y=y_cls,
        y_2=y_2_cls,
        z=z_cls,
        z_2=z_2_cls,
        magnitude=magnitude_cls,
    )

