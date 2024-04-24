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

from .system_coupling_1 import system_coupling as system_coupling_cls
from .velocity_specification_method import velocity_specification_method as velocity_specification_method_cls
from .reference_frame_6 import reference_frame as reference_frame_cls
from .velocity_1 import velocity as velocity_cls
from .initial_gauge_pressure import initial_gauge_pressure as initial_gauge_pressure_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .velocity_components import velocity_components as velocity_components_cls
from .flow_direction import flow_direction as flow_direction_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .swirl_angular_velocity import swirl_angular_velocity as swirl_angular_velocity_cls
from .gauge_pressure import gauge_pressure as gauge_pressure_cls
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
        ['system_coupling', 'velocity_specification_method',
         'reference_frame', 'velocity', 'initial_gauge_pressure',
         'coordinate_system', 'velocity_components', 'flow_direction',
         'axis_direction', 'axis_origin', 'swirl_angular_velocity',
         'gauge_pressure', 'acoustic_wave_model', 'impedance_zero_order_term',
         'real_pole_series', 'complex_pole_series', 'incoming_wave']

    _child_classes = dict(
        system_coupling=system_coupling_cls,
        velocity_specification_method=velocity_specification_method_cls,
        reference_frame=reference_frame_cls,
        velocity=velocity_cls,
        initial_gauge_pressure=initial_gauge_pressure_cls,
        coordinate_system=coordinate_system_cls,
        velocity_components=velocity_components_cls,
        flow_direction=flow_direction_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        swirl_angular_velocity=swirl_angular_velocity_cls,
        gauge_pressure=gauge_pressure_cls,
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
        flow_direction_component="flow_direction",
        frame_of_reference="reference_frame",
        impedance_0="impedance_zero_order_term",
        impedance_1="real_pole_series",
        impedance_2="complex_pole_series",
        omega_swirl="swirl_angular_velocity",
        p="gauge_pressure",
        p_sup="initial_gauge_pressure",
        velocity_component="velocity_components",
        velocity_spec="velocity_specification_method",
        vmag="velocity",
    )

