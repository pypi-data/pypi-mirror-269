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

from .monitor_3 import monitor as monitor_cls
from .autosave_1 import autosave as autosave_cls
class calculation_activities(Group):
    """
    Calculation activities menu.
    """

    fluent_name = "calculation-activities"

    child_names = \
        ['monitor', 'autosave']

    _child_classes = dict(
        monitor=monitor_cls,
        autosave=autosave_cls,
    )

