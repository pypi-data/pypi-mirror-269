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
from .backflow_reference_frame import backflow_reference_frame as backflow_reference_frame_cls
from .pressure_spec import pressure_spec as pressure_spec_cls
from .pressure_spec_method import pressure_spec_method as pressure_spec_method_cls
from .gauge_pressure import gauge_pressure as gauge_pressure_cls
from .pressure_profile_multiplier import pressure_profile_multiplier as pressure_profile_multiplier_cls
from .backflow_dir_spec_method import backflow_dir_spec_method as backflow_dir_spec_method_cls
from .coordinate_system import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .backflow_pressure_spec import backflow_pressure_spec as backflow_pressure_spec_cls
from .backflow_pressure_specification import backflow_pressure_specification as backflow_pressure_specification_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .prevent_reverse_flow import prevent_reverse_flow as prevent_reverse_flow_cls
from .radial_equ_pressure_distribution import radial_equ_pressure_distribution as radial_equ_pressure_distribution_cls
from .avg_pressure_spec import avg_pressure_spec as avg_pressure_spec_cls
from .avg_method import avg_method as avg_method_cls
from .target_mass_flow_rate import target_mass_flow_rate as target_mass_flow_rate_cls
from .target_mass_flow import target_mass_flow as target_mass_flow_cls
from .upper_limit_of_abs_pressure import upper_limit_of_abs_pressure as upper_limit_of_abs_pressure_cls
from .lower_limit_of_abs_pressure import lower_limit_of_abs_pressure as lower_limit_of_abs_pressure_cls
from .acoustic_wave_model import acoustic_wave_model as acoustic_wave_model_cls
from .exit_pressure_spec import exit_pressure_spec as exit_pressure_spec_cls
from .impedance_zero_order_term import impedance_zero_order_term as impedance_zero_order_term_cls
from .real_pole_series import real_pole_series as real_pole_series_cls
from .complex_pole_series import complex_pole_series as complex_pole_series_cls
from .incoming_wave import incoming_wave as incoming_wave_cls
from .loss_coefficient import loss_coefficient as loss_coefficient_cls
from .strength import strength as strength_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['system_coupling', 'backflow_reference_frame', 'pressure_spec',
         'pressure_spec_method', 'gauge_pressure',
         'pressure_profile_multiplier', 'backflow_dir_spec_method',
         'coordinate_system', 'flow_direction', 'backflow_pressure_spec',
         'backflow_pressure_specification', 'axis_direction', 'axis_origin',
         'prevent_reverse_flow', 'radial_equ_pressure_distribution',
         'avg_pressure_spec', 'avg_method', 'target_mass_flow_rate',
         'target_mass_flow', 'upper_limit_of_abs_pressure',
         'lower_limit_of_abs_pressure', 'acoustic_wave_model',
         'exit_pressure_spec', 'impedance_zero_order_term',
         'real_pole_series', 'complex_pole_series', 'incoming_wave',
         'loss_coefficient', 'strength']

    _child_classes = dict(
        system_coupling=system_coupling_cls,
        backflow_reference_frame=backflow_reference_frame_cls,
        pressure_spec=pressure_spec_cls,
        pressure_spec_method=pressure_spec_method_cls,
        gauge_pressure=gauge_pressure_cls,
        pressure_profile_multiplier=pressure_profile_multiplier_cls,
        backflow_dir_spec_method=backflow_dir_spec_method_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        backflow_pressure_spec=backflow_pressure_spec_cls,
        backflow_pressure_specification=backflow_pressure_specification_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        prevent_reverse_flow=prevent_reverse_flow_cls,
        radial_equ_pressure_distribution=radial_equ_pressure_distribution_cls,
        avg_pressure_spec=avg_pressure_spec_cls,
        avg_method=avg_method_cls,
        target_mass_flow_rate=target_mass_flow_rate_cls,
        target_mass_flow=target_mass_flow_cls,
        upper_limit_of_abs_pressure=upper_limit_of_abs_pressure_cls,
        lower_limit_of_abs_pressure=lower_limit_of_abs_pressure_cls,
        acoustic_wave_model=acoustic_wave_model_cls,
        exit_pressure_spec=exit_pressure_spec_cls,
        impedance_zero_order_term=impedance_zero_order_term_cls,
        real_pole_series=real_pole_series_cls,
        complex_pole_series=complex_pole_series_cls,
        incoming_wave=incoming_wave_cls,
        loss_coefficient=loss_coefficient_cls,
        strength=strength_cls,
    )

    _child_aliases = dict(
        ac_options="acoustic_wave_model",
        ac_wave="incoming_wave",
        avg_option="avg_method",
        avg_press_spec="avg_pressure_spec",
        axis_direction_component="axis_direction",
        axis_origin_component="axis_origin",
        b="loss_coefficient",
        direction_spec="backflow_dir_spec_method",
        flow_direction_component="flow_direction",
        frame_of_reference="backflow_reference_frame",
        gen_nrbc_spec="exit_pressure_spec",
        impedance_0="impedance_zero_order_term",
        impedance_1="real_pole_series",
        impedance_2="complex_pole_series",
        p="gauge_pressure",
        p_backflow_spec="backflow_pressure_specification",
        p_backflow_spec_gen="backflow_pressure_spec",
        p_profile_multiplier="pressure_profile_multiplier",
        press_spec="pressure_spec_method",
        press_spec_gen="pressure_spec",
        radial="radial_equ_pressure_distribution",
        targeted_mf="target_mass_flow",
        targeted_mf_boundary="target_mass_flow_rate",
        targeted_mf_pmax="upper_limit_of_abs_pressure",
        targeted_mf_pmin="lower_limit_of_abs_pressure",
    )

