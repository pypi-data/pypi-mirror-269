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

from .pole import pole as pole_cls
from .amplitude import amplitude as amplitude_cls
class real_pole_series_child(Group):
    """
    'child_object_type' of real_pole_series.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['pole', 'amplitude']

    _child_classes = dict(
        pole=pole_cls,
        amplitude=amplitude_cls,
    )

