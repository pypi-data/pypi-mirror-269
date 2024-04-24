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

from .open_channel_wave_bc import open_channel_wave_bc as open_channel_wave_bc_cls
from .segregated_velocity_inputs import segregated_velocity_inputs as segregated_velocity_inputs_cls
from .averaged_flow_specification_method import averaged_flow_specification_method as averaged_flow_specification_method_cls
from .avg_flow_velocity import avg_flow_velocity as avg_flow_velocity_cls
from .flow_velocity import flow_velocity as flow_velocity_cls
from .moving_object_velocity_specification_method import moving_object_velocity_specification_method as moving_object_velocity_specification_method_cls
from .moving_object_velocity import moving_object_velocity as moving_object_velocity_cls
from .moving_object_direction import moving_object_direction as moving_object_direction_cls
from .secondary_phase_velocity_specification_method import secondary_phase_velocity_specification_method as secondary_phase_velocity_specification_method_cls
from .secondary_phase_velocity import secondary_phase_velocity as secondary_phase_velocity_cls
from .secondary_phase_direction import secondary_phase_direction as secondary_phase_direction_cls
from .primary_phase_velocity_specification_method import primary_phase_velocity_specification_method as primary_phase_velocity_specification_method_cls
from .primary_phase_reference_height_above_free_surface import primary_phase_reference_height_above_free_surface as primary_phase_reference_height_above_free_surface_cls
from .primary_phase_power_law_coefficient import primary_phase_power_law_coefficient as primary_phase_power_law_coefficient_cls
from .primary_phase_velocity import primary_phase_velocity as primary_phase_velocity_cls
from .primary_phase_reference_velocity import primary_phase_reference_velocity as primary_phase_reference_velocity_cls
from .primary_phase_direction import primary_phase_direction as primary_phase_direction_cls
from .secondary_phase_for_inlet import secondary_phase_for_inlet as secondary_phase_for_inlet_cls
from .wave_option import wave_option as wave_option_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .bottom_level import bottom_level as bottom_level_cls
from .reference_wave_direction import reference_wave_direction as reference_wave_direction_cls
from .reference_direction import reference_direction as reference_direction_cls
from .wave_modeling_option import wave_modeling_option as wave_modeling_option_cls
from .wave_group_inputs import wave_group_inputs as wave_group_inputs_cls
from .shallow_wave_inputs import shallow_wave_inputs as shallow_wave_inputs_cls
from .frequency_spectrum_method import frequency_spectrum_method as frequency_spectrum_method_cls
from .peak_shape_parameter import peak_shape_parameter as peak_shape_parameter_cls
from .significant_wave_height import significant_wave_height as significant_wave_height_cls
from .peak_frequency import peak_frequency as peak_frequency_cls
from .minimum_frequency import minimum_frequency as minimum_frequency_cls
from .maximum_frequency import maximum_frequency as maximum_frequency_cls
from .number_of_frequency_components import number_of_frequency_components as number_of_frequency_components_cls
from .directional_spreading_method import directional_spreading_method as directional_spreading_method_cls
from .frequency_independent_cosine_exponent import frequency_independent_cosine_exponent as frequency_independent_cosine_exponent_cls
from .mean_wave_heading_angle import mean_wave_heading_angle as mean_wave_heading_angle_cls
from .angular_deviation import angular_deviation as angular_deviation_cls
from .angular_components_count import angular_components_count as angular_components_count_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration import interfacial_area_concentration as interfacial_area_concentration_cls
from .level_set_function_flux import level_set_function_flux as level_set_function_flux_cls
from .volume_fraction import volume_fraction as volume_fraction_cls
from .discrete_boundary_condition import discrete_boundary_condition as discrete_boundary_condition_cls
from .pb_disc import pb_disc as pb_disc_cls
from .quadrature_moment_boundary_condition import quadrature_moment_boundary_condition as quadrature_moment_boundary_condition_cls
from .quadrature_moment_boundary_value import quadrature_moment_boundary_value as quadrature_moment_boundary_value_cls
from .qbmm_boundary_condition import qbmm_boundary_condition as qbmm_boundary_condition_cls
from .qbmm_boundary_value import qbmm_boundary_value as qbmm_boundary_value_cls
from .std_moment_boundary_condition import std_moment_boundary_condition as std_moment_boundary_condition_cls
from .std_moment_boundary_value import std_moment_boundary_value as std_moment_boundary_value_cls
from .dqmom_boundary_condition import dqmom_boundary_condition as dqmom_boundary_condition_cls
from .dqmom_boundary_value import dqmom_boundary_value as dqmom_boundary_value_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel_wave_bc', 'segregated_velocity_inputs',
         'averaged_flow_specification_method', 'avg_flow_velocity',
         'flow_velocity', 'moving_object_velocity_specification_method',
         'moving_object_velocity', 'moving_object_direction',
         'secondary_phase_velocity_specification_method',
         'secondary_phase_velocity', 'secondary_phase_direction',
         'primary_phase_velocity_specification_method',
         'primary_phase_reference_height_above_free_surface',
         'primary_phase_power_law_coefficient', 'primary_phase_velocity',
         'primary_phase_reference_velocity', 'primary_phase_direction',
         'secondary_phase_for_inlet', 'wave_option', 'free_surface_level',
         'bottom_level', 'reference_wave_direction', 'reference_direction',
         'wave_modeling_option', 'wave_group_inputs', 'shallow_wave_inputs',
         'frequency_spectrum_method', 'peak_shape_parameter',
         'significant_wave_height', 'peak_frequency', 'minimum_frequency',
         'maximum_frequency', 'number_of_frequency_components',
         'directional_spreading_method',
         'frequency_independent_cosine_exponent', 'mean_wave_heading_angle',
         'angular_deviation', 'angular_components_count',
         'granular_temperature', 'interfacial_area_concentration',
         'level_set_function_flux', 'volume_fraction',
         'discrete_boundary_condition', 'pb_disc',
         'quadrature_moment_boundary_condition',
         'quadrature_moment_boundary_value', 'qbmm_boundary_condition',
         'qbmm_boundary_value', 'std_moment_boundary_condition',
         'std_moment_boundary_value', 'dqmom_boundary_condition',
         'dqmom_boundary_value']

    _child_classes = dict(
        open_channel_wave_bc=open_channel_wave_bc_cls,
        segregated_velocity_inputs=segregated_velocity_inputs_cls,
        averaged_flow_specification_method=averaged_flow_specification_method_cls,
        avg_flow_velocity=avg_flow_velocity_cls,
        flow_velocity=flow_velocity_cls,
        moving_object_velocity_specification_method=moving_object_velocity_specification_method_cls,
        moving_object_velocity=moving_object_velocity_cls,
        moving_object_direction=moving_object_direction_cls,
        secondary_phase_velocity_specification_method=secondary_phase_velocity_specification_method_cls,
        secondary_phase_velocity=secondary_phase_velocity_cls,
        secondary_phase_direction=secondary_phase_direction_cls,
        primary_phase_velocity_specification_method=primary_phase_velocity_specification_method_cls,
        primary_phase_reference_height_above_free_surface=primary_phase_reference_height_above_free_surface_cls,
        primary_phase_power_law_coefficient=primary_phase_power_law_coefficient_cls,
        primary_phase_velocity=primary_phase_velocity_cls,
        primary_phase_reference_velocity=primary_phase_reference_velocity_cls,
        primary_phase_direction=primary_phase_direction_cls,
        secondary_phase_for_inlet=secondary_phase_for_inlet_cls,
        wave_option=wave_option_cls,
        free_surface_level=free_surface_level_cls,
        bottom_level=bottom_level_cls,
        reference_wave_direction=reference_wave_direction_cls,
        reference_direction=reference_direction_cls,
        wave_modeling_option=wave_modeling_option_cls,
        wave_group_inputs=wave_group_inputs_cls,
        shallow_wave_inputs=shallow_wave_inputs_cls,
        frequency_spectrum_method=frequency_spectrum_method_cls,
        peak_shape_parameter=peak_shape_parameter_cls,
        significant_wave_height=significant_wave_height_cls,
        peak_frequency=peak_frequency_cls,
        minimum_frequency=minimum_frequency_cls,
        maximum_frequency=maximum_frequency_cls,
        number_of_frequency_components=number_of_frequency_components_cls,
        directional_spreading_method=directional_spreading_method_cls,
        frequency_independent_cosine_exponent=frequency_independent_cosine_exponent_cls,
        mean_wave_heading_angle=mean_wave_heading_angle_cls,
        angular_deviation=angular_deviation_cls,
        angular_components_count=angular_components_count_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        level_set_function_flux=level_set_function_flux_cls,
        volume_fraction=volume_fraction_cls,
        discrete_boundary_condition=discrete_boundary_condition_cls,
        pb_disc=pb_disc_cls,
        quadrature_moment_boundary_condition=quadrature_moment_boundary_condition_cls,
        quadrature_moment_boundary_value=quadrature_moment_boundary_value_cls,
        qbmm_boundary_condition=qbmm_boundary_condition_cls,
        qbmm_boundary_value=qbmm_boundary_value_cls,
        std_moment_boundary_condition=std_moment_boundary_condition_cls,
        std_moment_boundary_value=std_moment_boundary_value_cls,
        dqmom_boundary_condition=dqmom_boundary_condition_cls,
        dqmom_boundary_value=dqmom_boundary_value_cls,
    )

    _child_aliases = dict(
        ht_bottom="bottom_level",
        ht_local="free_surface_level",
        iac="interfacial_area_concentration",
        lsfun="level_set_function_flux",
        moving_object_direction_components="moving_object_direction",
        ocw_pp_power_coeff="primary_phase_power_law_coefficient",
        ocw_pp_ref_ht="primary_phase_reference_height_above_free_surface",
        ocw_pp_vel_spec="primary_phase_velocity_specification_method",
        ocw_pp_vmag="primary_phase_velocity",
        ocw_pp_vmag_ref="primary_phase_reference_velocity",
        ocw_ship_vel_spec="moving_object_velocity_specification_method",
        ocw_ship_vmag="moving_object_velocity",
        ocw_sp_vel_spec="secondary_phase_velocity_specification_method",
        ocw_sp_vmag="secondary_phase_velocity",
        ocw_vel_segregated="segregated_velocity_inputs",
        open_channel_wave_bc="open_channel_wave_bc",
        pb_disc_bc="discrete_boundary_condition",
        pb_dqmom="dqmom_boundary_value",
        pb_dqmom_bc="dqmom_boundary_condition",
        pb_qbmm="qbmm_boundary_value",
        pb_qbmm_bc="qbmm_boundary_condition",
        pb_qmom="quadrature_moment_boundary_value",
        pb_qmom_bc="quadrature_moment_boundary_condition",
        pb_smm="std_moment_boundary_value",
        pb_smm_bc="std_moment_boundary_condition",
        phase_spec="secondary_phase_for_inlet",
        primary_phase_direction_components="primary_phase_direction",
        secondary_phase_direction_components="secondary_phase_direction",
        wave_bc_type="wave_option",
        wave_components="flow_velocity",
        wave_dir_spec="reference_wave_direction",
        wave_list="wave_group_inputs",
        wave_list_shallow="shallow_wave_inputs",
        wave_modeling_type="wave_modeling_option",
        wave_spect_deviation="angular_deviation",
        wave_spect_dir_components="angular_components_count",
        wave_spect_factor="peak_shape_parameter",
        wave_spect_freq_components="number_of_frequency_components",
        wave_spect_max_freq="maximum_frequency",
        wave_spect_mean_angle="mean_wave_heading_angle",
        wave_spect_method_dir="directional_spreading_method",
        wave_spect_method_freq="frequency_spectrum_method",
        wave_spect_min_freq="minimum_frequency",
        wave_spect_peak_freq="peak_frequency",
        wave_spect_s="frequency_independent_cosine_exponent",
        wave_spect_sig_wave_ht="significant_wave_height",
        wave_velocity_spec="averaged_flow_specification_method",
        wave_vmag="avg_flow_velocity",
    )

