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

from .prescribed import prescribed as prescribed_cls
from .value_16 import value as value_cls
class axis_2(Group):
    """
    Prescribed scaling factor for axis 2.
    """

    fluent_name = "axis-2"

    child_names = \
        ['prescribed', 'value']

    _child_classes = dict(
        prescribed=prescribed_cls,
        value=value_cls,
    )

