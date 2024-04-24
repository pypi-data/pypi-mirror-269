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

from .accuracy_control import accuracy_control as accuracy_control_cls
from .option_7 import option as option_cls
from .low_order_scheme import low_order_scheme as low_order_scheme_cls
from .high_order_scheme import high_order_scheme as high_order_scheme_cls
class tracking(Group):
    """
    Group containing DPM tracking related settings.
    """

    fluent_name = "tracking"

    child_names = \
        ['accuracy_control', 'option', 'low_order_scheme',
         'high_order_scheme']

    _child_classes = dict(
        accuracy_control=accuracy_control_cls,
        option=option_cls,
        low_order_scheme=low_order_scheme_cls,
        high_order_scheme=high_order_scheme_cls,
    )

    _child_aliases = dict(
        scheme="option",
    )

