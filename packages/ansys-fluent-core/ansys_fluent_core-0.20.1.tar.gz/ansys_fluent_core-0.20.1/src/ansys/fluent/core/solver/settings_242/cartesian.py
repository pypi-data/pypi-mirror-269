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

from .extent import extent as extent_cls
from .conditions import conditions as conditions_cls
class cartesian(Group):
    """
    Design tool cartesian region menu.
    """

    fluent_name = "cartesian"

    child_names = \
        ['extent', 'conditions']

    _child_classes = dict(
        extent=extent_cls,
        conditions=conditions_cls,
    )

