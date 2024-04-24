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

from .x_1 import x as x_cls
from .y_1 import y as y_cls
from .z_1 import z as z_cls
class r(Group):
    """
    'r' child.
    """

    fluent_name = "r"

    child_names = \
        ['x', 'y', 'z']

    _child_classes = dict(
        x=x_cls,
        y=y_cls,
        z=z_cls,
    )

