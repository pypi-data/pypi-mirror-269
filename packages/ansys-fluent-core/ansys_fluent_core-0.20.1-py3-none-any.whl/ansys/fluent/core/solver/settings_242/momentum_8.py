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

from .reference_frame_4 import reference_frame as reference_frame_cls
from .gauge_total_pressure import gauge_total_pressure as gauge_total_pressure_cls
from .supersonic_or_initial_gauge_pressure import supersonic_or_initial_gauge_pressure as supersonic_or_initial_gauge_pressure_cls
from .direction_specification_method import direction_specification_method as direction_specification_method_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .prevent_reverse_flow_1 import prevent_reverse_flow as prevent_reverse_flow_cls
from .acoustic_wave_model import acoustic_wave_model as acoustic_wave_model_cls
from .impedance_zero_order_term import impedance_zero_order_term as impedance_zero_order_term_cls
from .real_pole_series import real_pole_series as real_pole_series_cls
from .complex_pole_series import complex_pole_series as complex_pole_series_cls
from .incoming_wave import incoming_wave as incoming_wave_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['reference_frame', 'gauge_total_pressure',
         'supersonic_or_initial_gauge_pressure',
         'direction_specification_method', 'coordinate_system',
         'flow_direction', 'direction_vector', 'axis_direction',
         'axis_origin', 'prevent_reverse_flow', 'acoustic_wave_model',
         'impedance_zero_order_term', 'real_pole_series',
         'complex_pole_series', 'incoming_wave']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        gauge_total_pressure=gauge_total_pressure_cls,
        supersonic_or_initial_gauge_pressure=supersonic_or_initial_gauge_pressure_cls,
        direction_specification_method=direction_specification_method_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        prevent_reverse_flow=prevent_reverse_flow_cls,
        acoustic_wave_model=acoustic_wave_model_cls,
        impedance_zero_order_term=impedance_zero_order_term_cls,
        real_pole_series=real_pole_series_cls,
        complex_pole_series=complex_pole_series_cls,
        incoming_wave=incoming_wave_cls,
    )

    _child_aliases = dict(
        ac_options="acoustic_wave_model",
        ac_wave="incoming_wave",
        axis_direction_component="axis_direction",
        axis_origin_component="axis_origin",
        direction_spec="direction_specification_method",
        direction_vector_components="direction_vector",
        flow_direction_component="flow_direction",
        frame_of_reference="reference_frame",
        impedance_0="impedance_zero_order_term",
        impedance_1="real_pole_series",
        impedance_2="complex_pole_series",
        p0="gauge_total_pressure",
    )

