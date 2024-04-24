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

from .coordinate_system_2 import coordinate_system as coordinate_system_cls
from .extent_1 import extent as extent_cls
from .conditions import conditions as conditions_cls
class cylindrical(Group):
    """
    Design tool cartesian region menu.
    """

    fluent_name = "cylindrical"

    child_names = \
        ['coordinate_system', 'extent', 'conditions']

    _child_classes = dict(
        coordinate_system=coordinate_system_cls,
        extent=extent_cls,
        conditions=conditions_cls,
    )

