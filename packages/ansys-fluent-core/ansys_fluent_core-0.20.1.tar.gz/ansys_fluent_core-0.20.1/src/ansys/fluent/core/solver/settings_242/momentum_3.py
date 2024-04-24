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

from .reference_frame_5 import reference_frame as reference_frame_cls
from .system_coupling_1 import system_coupling as system_coupling_cls
from .mass_flow_specification import mass_flow_specification as mass_flow_specification_cls
from .mass_flow_rate_1 import mass_flow_rate as mass_flow_rate_cls
from .exit_corrected_mass_flow_rate import exit_corrected_mass_flow_rate as exit_corrected_mass_flow_rate_cls
from .mass_flux import mass_flux as mass_flux_cls
from .average_mass_flux import average_mass_flux as average_mass_flux_cls
from .supersonic_gauge_pressure import supersonic_gauge_pressure as supersonic_gauge_pressure_cls
from .direction_specification import direction_specification as direction_specification_cls
from .coordinate_system_1 import coordinate_system as coordinate_system_cls
from .flow_direction import flow_direction as flow_direction_cls
from .direction_vector import direction_vector as direction_vector_cls
from .axis_direction_2 import axis_direction as axis_direction_cls
from .axis_origin_2 import axis_origin as axis_origin_cls
from .swirl_velocity_specification_1 import swirl_velocity_specification as swirl_velocity_specification_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
from .fan_origin import fan_origin as fan_origin_cls
from .ecmf_reference_temperature import ecmf_reference_temperature as ecmf_reference_temperature_cls
from .ecmf_reference_gauge_pressure import ecmf_reference_gauge_pressure as ecmf_reference_gauge_pressure_cls
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
        ['reference_frame', 'system_coupling', 'mass_flow_specification',
         'mass_flow_rate', 'exit_corrected_mass_flow_rate', 'mass_flux',
         'average_mass_flux', 'supersonic_gauge_pressure',
         'direction_specification', 'coordinate_system', 'flow_direction',
         'direction_vector', 'axis_direction', 'axis_origin',
         'swirl_velocity_specification', 'swirl_factor', 'fan_origin',
         'ecmf_reference_temperature', 'ecmf_reference_gauge_pressure',
         'acoustic_wave_model', 'impedance_zero_order_term',
         'real_pole_series', 'complex_pole_series', 'incoming_wave']

    _child_classes = dict(
        reference_frame=reference_frame_cls,
        system_coupling=system_coupling_cls,
        mass_flow_specification=mass_flow_specification_cls,
        mass_flow_rate=mass_flow_rate_cls,
        exit_corrected_mass_flow_rate=exit_corrected_mass_flow_rate_cls,
        mass_flux=mass_flux_cls,
        average_mass_flux=average_mass_flux_cls,
        supersonic_gauge_pressure=supersonic_gauge_pressure_cls,
        direction_specification=direction_specification_cls,
        coordinate_system=coordinate_system_cls,
        flow_direction=flow_direction_cls,
        direction_vector=direction_vector_cls,
        axis_direction=axis_direction_cls,
        axis_origin=axis_origin_cls,
        swirl_velocity_specification=swirl_velocity_specification_cls,
        swirl_factor=swirl_factor_cls,
        fan_origin=fan_origin_cls,
        ecmf_reference_temperature=ecmf_reference_temperature_cls,
        ecmf_reference_gauge_pressure=ecmf_reference_gauge_pressure_cls,
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
        direction_spec="direction_specification",
        direction_vector_components="direction_vector",
        ec_mass_flow="exit_corrected_mass_flow_rate",
        fan_origin_components="fan_origin",
        flow_direction_component="flow_direction",
        flow_spec="mass_flow_specification",
        frame_of_reference="reference_frame",
        impedance_0="impedance_zero_order_term",
        impedance_1="real_pole_series",
        impedance_2="complex_pole_series",
        mass_flow="mass_flow_rate",
        mass_flux_ave="average_mass_flux",
        p="supersonic_gauge_pressure",
        pref="ecmf_reference_gauge_pressure",
        swirl_model="swirl_velocity_specification",
        tref="ecmf_reference_temperature",
    )

