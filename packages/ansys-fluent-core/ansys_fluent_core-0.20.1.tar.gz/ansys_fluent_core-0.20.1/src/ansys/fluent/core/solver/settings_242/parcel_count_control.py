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

from .data_reduction import data_reduction as data_reduction_cls
class parcel_count_control(Group):
    """
    Specify options for increasing or decreasing the number of DPM numerical parcels to meet resolution requirements.
    """

    fluent_name = "parcel-count-control"

    child_names = \
        ['data_reduction']

    _child_classes = dict(
        data_reduction=data_reduction_cls,
    )

