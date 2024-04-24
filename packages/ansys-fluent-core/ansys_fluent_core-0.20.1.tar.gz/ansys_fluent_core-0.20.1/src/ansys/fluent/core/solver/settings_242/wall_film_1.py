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

from .eulerian_film_wall import eulerian_film_wall as eulerian_film_wall_cls
from .film_condition_type import film_condition_type as film_condition_type_cls
from .film_height import film_height as film_height_cls
from .flux_momentum import flux_momentum as flux_momentum_cls
from .relative_initial_film_velocity import relative_initial_film_velocity as relative_initial_film_velocity_cls
from .include_film_momentum_pressure import include_film_momentum_pressure as include_film_momentum_pressure_cls
from .film_temperature import film_temperature as film_temperature_cls
from .film_passive_scalar import film_passive_scalar as film_passive_scalar_cls
from .enable_film_source_terms import enable_film_source_terms as enable_film_source_terms_cls
from .film_mass_source import film_mass_source as film_mass_source_cls
from .momentum_source import momentum_source as momentum_source_cls
from .film_heat_source import film_heat_source as film_heat_source_cls
from .film_passive_scalar_source import film_passive_scalar_source as film_passive_scalar_source_cls
from .enable_film_phase_change import enable_film_phase_change as enable_film_phase_change_cls
from .phase_change_model import phase_change_model as phase_change_model_cls
from .film_condensation_constant import film_condensation_constant as film_condensation_constant_cls
from .film_vaporization_constant import film_vaporization_constant as film_vaporization_constant_cls
from .film_condensation_rate import film_condensation_rate as film_condensation_rate_cls
from .film_vaporization_rate import film_vaporization_rate as film_vaporization_rate_cls
from .enable_flow_momentum_coupling import enable_flow_momentum_coupling as enable_flow_momentum_coupling_cls
from .enable_dpm_wall_splash import enable_dpm_wall_splash as enable_dpm_wall_splash_cls
from .allow_film_boundary_separation import allow_film_boundary_separation as allow_film_boundary_separation_cls
from .impingement_model_1 import impingement_model as impingement_model_cls
from .number_of_splashed_particles import number_of_splashed_particles as number_of_splashed_particles_cls
from .critical_temperature_factor import critical_temperature_factor as critical_temperature_factor_cls
from .wall_roughness_length_ra import wall_roughness_length_ra as wall_roughness_length_ra_cls
from .wall_roughness_length_rz import wall_roughness_length_rz as wall_roughness_length_rz_cls
from .upper_deposition_limit_offset import upper_deposition_limit_offset as upper_deposition_limit_offset_cls
from .deposition_delta_t import deposition_delta_t as deposition_delta_t_cls
from .laplace_number_constant import laplace_number_constant as laplace_number_constant_cls
from .partial_evaporation_ratio import partial_evaporation_ratio as partial_evaporation_ratio_cls
from .enable_film_contact_angle_force import enable_film_contact_angle_force as enable_film_contact_angle_force_cls
from .film_contact_angle_mean import film_contact_angle_mean as film_contact_angle_mean_cls
from .film_contact_angle_rstd import film_contact_angle_rstd as film_contact_angle_rstd_cls
from .film_contact_angle_beta import film_contact_angle_beta as film_contact_angle_beta_cls
from .film_vof_coupling_high import film_vof_coupling_high as film_vof_coupling_high_cls
from .film_vof_trans_high import film_vof_trans_high as film_vof_trans_high_cls
from .film_vof_trans_high_relax import film_vof_trans_high_relax as film_vof_trans_high_relax_cls
from .film_vof_coupling_low import film_vof_coupling_low as film_vof_coupling_low_cls
from .film_vof_trans_low import film_vof_trans_low as film_vof_trans_low_cls
from .film_vof_trans_low_relax import film_vof_trans_low_relax as film_vof_trans_low_relax_cls
class wall_film(Group):
    """
    Wall Film Settings for boundary-condition.
    """

    fluent_name = "wall-film"

    child_names = \
        ['eulerian_film_wall', 'film_condition_type', 'film_height',
         'flux_momentum', 'relative_initial_film_velocity',
         'include_film_momentum_pressure', 'film_temperature',
         'film_passive_scalar', 'enable_film_source_terms',
         'film_mass_source', 'momentum_source', 'film_heat_source',
         'film_passive_scalar_source', 'enable_film_phase_change',
         'phase_change_model', 'film_condensation_constant',
         'film_vaporization_constant', 'film_condensation_rate',
         'film_vaporization_rate', 'enable_flow_momentum_coupling',
         'enable_dpm_wall_splash', 'allow_film_boundary_separation',
         'impingement_model', 'number_of_splashed_particles',
         'critical_temperature_factor', 'wall_roughness_length_ra',
         'wall_roughness_length_rz', 'upper_deposition_limit_offset',
         'deposition_delta_t', 'laplace_number_constant',
         'partial_evaporation_ratio', 'enable_film_contact_angle_force',
         'film_contact_angle_mean', 'film_contact_angle_rstd',
         'film_contact_angle_beta', 'film_vof_coupling_high',
         'film_vof_trans_high', 'film_vof_trans_high_relax',
         'film_vof_coupling_low', 'film_vof_trans_low',
         'film_vof_trans_low_relax']

    _child_classes = dict(
        eulerian_film_wall=eulerian_film_wall_cls,
        film_condition_type=film_condition_type_cls,
        film_height=film_height_cls,
        flux_momentum=flux_momentum_cls,
        relative_initial_film_velocity=relative_initial_film_velocity_cls,
        include_film_momentum_pressure=include_film_momentum_pressure_cls,
        film_temperature=film_temperature_cls,
        film_passive_scalar=film_passive_scalar_cls,
        enable_film_source_terms=enable_film_source_terms_cls,
        film_mass_source=film_mass_source_cls,
        momentum_source=momentum_source_cls,
        film_heat_source=film_heat_source_cls,
        film_passive_scalar_source=film_passive_scalar_source_cls,
        enable_film_phase_change=enable_film_phase_change_cls,
        phase_change_model=phase_change_model_cls,
        film_condensation_constant=film_condensation_constant_cls,
        film_vaporization_constant=film_vaporization_constant_cls,
        film_condensation_rate=film_condensation_rate_cls,
        film_vaporization_rate=film_vaporization_rate_cls,
        enable_flow_momentum_coupling=enable_flow_momentum_coupling_cls,
        enable_dpm_wall_splash=enable_dpm_wall_splash_cls,
        allow_film_boundary_separation=allow_film_boundary_separation_cls,
        impingement_model=impingement_model_cls,
        number_of_splashed_particles=number_of_splashed_particles_cls,
        critical_temperature_factor=critical_temperature_factor_cls,
        wall_roughness_length_ra=wall_roughness_length_ra_cls,
        wall_roughness_length_rz=wall_roughness_length_rz_cls,
        upper_deposition_limit_offset=upper_deposition_limit_offset_cls,
        deposition_delta_t=deposition_delta_t_cls,
        laplace_number_constant=laplace_number_constant_cls,
        partial_evaporation_ratio=partial_evaporation_ratio_cls,
        enable_film_contact_angle_force=enable_film_contact_angle_force_cls,
        film_contact_angle_mean=film_contact_angle_mean_cls,
        film_contact_angle_rstd=film_contact_angle_rstd_cls,
        film_contact_angle_beta=film_contact_angle_beta_cls,
        film_vof_coupling_high=film_vof_coupling_high_cls,
        film_vof_trans_high=film_vof_trans_high_cls,
        film_vof_trans_high_relax=film_vof_trans_high_relax_cls,
        film_vof_coupling_low=film_vof_coupling_low_cls,
        film_vof_trans_low=film_vof_trans_low_cls,
        film_vof_trans_low_relax=film_vof_trans_low_relax_cls,
    )

    _child_aliases = dict(
        film_a_wet="laplace_number_constant",
        film_bc_imp_press="include_film_momentum_pressure",
        film_boundary_separation="allow_film_boundary_separation",
        film_cond_const="film_condensation_constant",
        film_cond_rate="film_condensation_rate",
        film_contact_angle="enable_film_contact_angle_force",
        film_crit_temp_factor="critical_temperature_factor",
        film_h_src="film_mass_source",
        film_impinge_model="impingement_model",
        film_momentum_coupling="enable_flow_momentum_coupling",
        film_partial_evap_ratio="partial_evaporation_ratio",
        film_phase_change_model="phase_change_model",
        film_phase_change="enable_film_phase_change",
        film_relative_vel="relative_initial_film_velocity",
        film_roughness_ra="wall_roughness_length_ra",
        film_roughness_rz="wall_roughness_length_rz",
        film_s_src="film_passive_scalar_source",
        film_scalar="film_passive_scalar",
        film_source="enable_film_source_terms",
        film_splash_nparc="number_of_splashed_particles",
        film_splash_wall="enable_dpm_wall_splash",
        film_t_delta="deposition_delta_t",
        film_t_deposition_offset="upper_deposition_limit_offset",
        film_t_src="film_heat_source",
        film_vapo_const="film_vaporization_constant",
        film_vapo_rate="film_vaporization_rate",
        film_wall_bc="film_condition_type",
        film_wall="eulerian_film_wall",
        flux_momentum_components="flux_momentum",
        momentum_source_components="momentum_source",
    )

