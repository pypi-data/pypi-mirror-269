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

from .axis_1_1 import axis_1 as axis_1_cls
from .axis_2_1 import axis_2 as axis_2_cls
from .axis_3_1 import axis_3 as axis_3_cls
class axis_factor(Group):
    """
    Prescribed scaling factor for the various axis menu.
    """

    fluent_name = "axis-factor"

    child_names = \
        ['axis_1', 'axis_2', 'axis_3']

    _child_classes = dict(
        axis_1=axis_1_cls,
        axis_2=axis_2_cls,
        axis_3=axis_3_cls,
    )

