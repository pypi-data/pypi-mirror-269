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

from .data_reduction_time_first_execution import data_reduction_time_first_execution as data_reduction_time_first_execution_cls
from .data_reduction_time_interval import data_reduction_time_interval as data_reduction_time_interval_cls
from .target_num_parcels_per_face import target_num_parcels_per_face as target_num_parcels_per_face_cls
from .additional_velocity_intervals import additional_velocity_intervals as additional_velocity_intervals_cls
from .additional_temperature_intervals import additional_temperature_intervals as additional_temperature_intervals_cls
class data_reduction(Group):
    """
    Help not available.
    """

    fluent_name = "data-reduction"

    child_names = \
        ['data_reduction_time_first_execution',
         'data_reduction_time_interval', 'target_num_parcels_per_face',
         'additional_velocity_intervals', 'additional_temperature_intervals']

    _child_classes = dict(
        data_reduction_time_first_execution=data_reduction_time_first_execution_cls,
        data_reduction_time_interval=data_reduction_time_interval_cls,
        target_num_parcels_per_face=target_num_parcels_per_face_cls,
        additional_velocity_intervals=additional_velocity_intervals_cls,
        additional_temperature_intervals=additional_temperature_intervals_cls,
    )

