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
class x(Group):
    """
    Prescribed X displacement.
    """

    fluent_name = "x"

    child_names = \
        ['prescribed', 'value']

    _child_classes = dict(
        prescribed=prescribed_cls,
        value=value_cls,
    )

