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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .complex_pole_series_child import complex_pole_series_child

class complex_pole_series(ListObject[complex_pole_series_child]):
    """
    List of Complex Pole Series.
    """

    fluent_name = "complex-pole-series"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: complex_pole_series_child = complex_pole_series_child
    """
    child_object_type of complex_pole_series.
    """
