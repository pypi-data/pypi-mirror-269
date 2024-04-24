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
from .polar_data_pairs_child import polar_data_pairs_child

class polar_data_pairs(ListObject[polar_data_pairs_child]):
    """
    Specify polar data pairs.
    """

    fluent_name = "polar-data-pairs"

    command_names = \
        ['list_properties', 'resize']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
    )

    child_object_type: polar_data_pairs_child = polar_data_pairs_child
    """
    child_object_type of polar_data_pairs.
    """
