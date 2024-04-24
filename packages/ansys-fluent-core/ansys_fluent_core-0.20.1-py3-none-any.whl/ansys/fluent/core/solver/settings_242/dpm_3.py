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

from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .normal_coefficient import normal_coefficient as normal_coefficient_cls
from .tangential_coefficient import tangential_coefficient as tangential_coefficient_cls
from .dpm_bc_frictn_coeff import dpm_bc_frictn_coeff as dpm_bc_frictn_coeff_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .dpm_film_splash_nsamp import dpm_film_splash_nsamp as dpm_film_splash_nsamp_cls
from .dpm_crit_temp_option import dpm_crit_temp_option as dpm_crit_temp_option_cls
from .dpm_critical_temp_factor import dpm_critical_temp_factor as dpm_critical_temp_factor_cls
from .dpm_calibratable_temp import dpm_calibratable_temp as dpm_calibratable_temp_cls
from .dpm_impingement_splashing_model import dpm_impingement_splashing_model as dpm_impingement_splashing_model_cls
from .dpm_upper_deposition_limit_offset import dpm_upper_deposition_limit_offset as dpm_upper_deposition_limit_offset_cls
from .dpm_deposition_delta_t import dpm_deposition_delta_t as dpm_deposition_delta_t_cls
from .dpm_laplace_number_constant import dpm_laplace_number_constant as dpm_laplace_number_constant_cls
from .dpm_partial_evaporation_ratio import dpm_partial_evaporation_ratio as dpm_partial_evaporation_ratio_cls
from .ra_roughness import ra_roughness as ra_roughness_cls
from .rz_roughness import rz_roughness as rz_roughness_cls
from .rq_roughness import rq_roughness as rq_roughness_cls
from .rsm_roughness import rsm_roughness as rsm_roughness_cls
from .enable_generic_erosion_model import enable_generic_erosion_model as enable_generic_erosion_model_cls
from .generic_impact_angle_function import generic_impact_angle_function as generic_impact_angle_function_cls
from .generic_diameter_function import generic_diameter_function as generic_diameter_function_cls
from .generic_velocity_exponent_function import generic_velocity_exponent_function as generic_velocity_exponent_function_cls
from .enable_finnie_erosion_model import enable_finnie_erosion_model as enable_finnie_erosion_model_cls
from .dpm_bc_erosion_finnie_k import dpm_bc_erosion_finnie_k as dpm_bc_erosion_finnie_k_cls
from .dpm_bc_erosion_finnie_vel_exp import dpm_bc_erosion_finnie_vel_exp as dpm_bc_erosion_finnie_vel_exp_cls
from .dpm_bc_erosion_finnie_max_erosion_angle import dpm_bc_erosion_finnie_max_erosion_angle as dpm_bc_erosion_finnie_max_erosion_angle_cls
from .dpm_bc_erosion_mclaury import dpm_bc_erosion_mclaury as dpm_bc_erosion_mclaury_cls
from .dpm_bc_erosion_mclaury_a import dpm_bc_erosion_mclaury_a as dpm_bc_erosion_mclaury_a_cls
from .dpm_bc_erosion_mclaury_vel_exp import dpm_bc_erosion_mclaury_vel_exp as dpm_bc_erosion_mclaury_vel_exp_cls
from .dpm_bc_erosion_mclaury_transition_angle import dpm_bc_erosion_mclaury_transition_angle as dpm_bc_erosion_mclaury_transition_angle_cls
from .dpm_bc_erosion_mclaury_b import dpm_bc_erosion_mclaury_b as dpm_bc_erosion_mclaury_b_cls
from .dpm_bc_erosion_mclaury_c import dpm_bc_erosion_mclaury_c as dpm_bc_erosion_mclaury_c_cls
from .dpm_bc_erosion_mclaury_w import dpm_bc_erosion_mclaury_w as dpm_bc_erosion_mclaury_w_cls
from .dpm_bc_erosion_mclaury_x import dpm_bc_erosion_mclaury_x as dpm_bc_erosion_mclaury_x_cls
from .dpm_bc_erosion_mclaury_y import dpm_bc_erosion_mclaury_y as dpm_bc_erosion_mclaury_y_cls
from .dpm_bc_erosion_oka import dpm_bc_erosion_oka as dpm_bc_erosion_oka_cls
from .dpm_bc_erosion_oka_e90 import dpm_bc_erosion_oka_e90 as dpm_bc_erosion_oka_e90_cls
from .dpm_bc_erosion_oka_hv import dpm_bc_erosion_oka_hv as dpm_bc_erosion_oka_hv_cls
from .dpm_bc_erosion_oka_n1 import dpm_bc_erosion_oka_n1 as dpm_bc_erosion_oka_n1_cls
from .dpm_bc_erosion_oka_n2 import dpm_bc_erosion_oka_n2 as dpm_bc_erosion_oka_n2_cls
from .dpm_bc_erosion_oka_k2 import dpm_bc_erosion_oka_k2 as dpm_bc_erosion_oka_k2_cls
from .dpm_bc_erosion_oka_k3 import dpm_bc_erosion_oka_k3 as dpm_bc_erosion_oka_k3_cls
from .dpm_bc_erosion_oka_dref import dpm_bc_erosion_oka_dref as dpm_bc_erosion_oka_dref_cls
from .dpm_bc_erosion_oka_vref import dpm_bc_erosion_oka_vref as dpm_bc_erosion_oka_vref_cls
from .dpm_bc_erosion_dnv import dpm_bc_erosion_dnv as dpm_bc_erosion_dnv_cls
from .dpm_bc_erosion_dnv_k import dpm_bc_erosion_dnv_k as dpm_bc_erosion_dnv_k_cls
from .dpm_bc_erosion_dnv_n import dpm_bc_erosion_dnv_n as dpm_bc_erosion_dnv_n_cls
from .dpm_bc_erosion_dnv_ductile import dpm_bc_erosion_dnv_ductile as dpm_bc_erosion_dnv_ductile_cls
from .dpm_bc_erosion_shear import dpm_bc_erosion_shear as dpm_bc_erosion_shear_cls
from .dpm_bc_erosion_shear_v import dpm_bc_erosion_shear_v as dpm_bc_erosion_shear_v_cls
from .dpm_bc_erosion_shear_c import dpm_bc_erosion_shear_c as dpm_bc_erosion_shear_c_cls
from .dpm_bc_erosion_shear_packing_limit import dpm_bc_erosion_shear_packing_limit as dpm_bc_erosion_shear_packing_limit_cls
from .dpm_bc_erosion_shielding import dpm_bc_erosion_shielding as dpm_bc_erosion_shielding_cls
from .dpm_wall_heat_exchange import dpm_wall_heat_exchange as dpm_wall_heat_exchange_cls
from .dpm_film_condensation import dpm_film_condensation as dpm_film_condensation_cls
from .dpm_film_bl_model import dpm_film_bl_model as dpm_film_bl_model_cls
from .dpm_particle_stripping import dpm_particle_stripping as dpm_particle_stripping_cls
from .dpm_critical_shear_stress import dpm_critical_shear_stress as dpm_critical_shear_stress_cls
from .dpm_film_separation_model import dpm_film_separation_model as dpm_film_separation_model_cls
from .dpm_critical_we_number import dpm_critical_we_number as dpm_critical_we_number_cls
from .dpm_film_separation_angle import dpm_film_separation_angle as dpm_film_separation_angle_cls
from .dpm_allow_lwf_to_vof import dpm_allow_lwf_to_vof as dpm_allow_lwf_to_vof_cls
from .dpm_allow_vof_to_lwf import dpm_allow_vof_to_lwf as dpm_allow_vof_to_lwf_cls
from .dpm_initialize_lwf import dpm_initialize_lwf as dpm_initialize_lwf_cls
from .dpm_initial_height import dpm_initial_height as dpm_initial_height_cls
from .film_velocity import film_velocity as film_velocity_cls
from .dpm_initial_temperature import dpm_initial_temperature as dpm_initial_temperature_cls
from .dpm_initial_injection import dpm_initial_injection as dpm_initial_injection_cls
from .film_parcel_surface_area_density import film_parcel_surface_area_density as film_parcel_surface_area_density_cls
from .minimum_number_of_parcels_per_face import minimum_number_of_parcels_per_face as minimum_number_of_parcels_per_face_cls
from .in_situ_data_reduction import in_situ_data_reduction as in_situ_data_reduction_cls
from .data_reduction_1 import data_reduction as data_reduction_cls
from .initialize_lwf_now import initialize_lwf_now as initialize_lwf_now_cls
class dpm(Group):
    """
    Help not available.
    """

    fluent_name = "dpm"

    child_names = \
        ['discrete_phase_bc_type', 'dem_collision_partner', 'reinj_inj',
         'normal_coefficient', 'tangential_coefficient',
         'dpm_bc_frictn_coeff', 'discrete_phase_bc_function',
         'dpm_film_splash_nsamp', 'dpm_crit_temp_option',
         'dpm_critical_temp_factor', 'dpm_calibratable_temp',
         'dpm_impingement_splashing_model',
         'dpm_upper_deposition_limit_offset', 'dpm_deposition_delta_t',
         'dpm_laplace_number_constant', 'dpm_partial_evaporation_ratio',
         'ra_roughness', 'rz_roughness', 'rq_roughness', 'rsm_roughness',
         'enable_generic_erosion_model', 'generic_impact_angle_function',
         'generic_diameter_function', 'generic_velocity_exponent_function',
         'enable_finnie_erosion_model', 'dpm_bc_erosion_finnie_k',
         'dpm_bc_erosion_finnie_vel_exp',
         'dpm_bc_erosion_finnie_max_erosion_angle', 'dpm_bc_erosion_mclaury',
         'dpm_bc_erosion_mclaury_a', 'dpm_bc_erosion_mclaury_vel_exp',
         'dpm_bc_erosion_mclaury_transition_angle',
         'dpm_bc_erosion_mclaury_b', 'dpm_bc_erosion_mclaury_c',
         'dpm_bc_erosion_mclaury_w', 'dpm_bc_erosion_mclaury_x',
         'dpm_bc_erosion_mclaury_y', 'dpm_bc_erosion_oka',
         'dpm_bc_erosion_oka_e90', 'dpm_bc_erosion_oka_hv',
         'dpm_bc_erosion_oka_n1', 'dpm_bc_erosion_oka_n2',
         'dpm_bc_erosion_oka_k2', 'dpm_bc_erosion_oka_k3',
         'dpm_bc_erosion_oka_dref', 'dpm_bc_erosion_oka_vref',
         'dpm_bc_erosion_dnv', 'dpm_bc_erosion_dnv_k', 'dpm_bc_erosion_dnv_n',
         'dpm_bc_erosion_dnv_ductile', 'dpm_bc_erosion_shear',
         'dpm_bc_erosion_shear_v', 'dpm_bc_erosion_shear_c',
         'dpm_bc_erosion_shear_packing_limit', 'dpm_bc_erosion_shielding',
         'dpm_wall_heat_exchange', 'dpm_film_condensation',
         'dpm_film_bl_model', 'dpm_particle_stripping',
         'dpm_critical_shear_stress', 'dpm_film_separation_model',
         'dpm_critical_we_number', 'dpm_film_separation_angle',
         'dpm_allow_lwf_to_vof', 'dpm_allow_vof_to_lwf', 'dpm_initialize_lwf',
         'dpm_initial_height', 'film_velocity', 'dpm_initial_temperature',
         'dpm_initial_injection', 'film_parcel_surface_area_density',
         'minimum_number_of_parcels_per_face', 'in_situ_data_reduction',
         'data_reduction']

    command_names = \
        ['initialize_lwf_now']

    _child_classes = dict(
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        normal_coefficient=normal_coefficient_cls,
        tangential_coefficient=tangential_coefficient_cls,
        dpm_bc_frictn_coeff=dpm_bc_frictn_coeff_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        dpm_film_splash_nsamp=dpm_film_splash_nsamp_cls,
        dpm_crit_temp_option=dpm_crit_temp_option_cls,
        dpm_critical_temp_factor=dpm_critical_temp_factor_cls,
        dpm_calibratable_temp=dpm_calibratable_temp_cls,
        dpm_impingement_splashing_model=dpm_impingement_splashing_model_cls,
        dpm_upper_deposition_limit_offset=dpm_upper_deposition_limit_offset_cls,
        dpm_deposition_delta_t=dpm_deposition_delta_t_cls,
        dpm_laplace_number_constant=dpm_laplace_number_constant_cls,
        dpm_partial_evaporation_ratio=dpm_partial_evaporation_ratio_cls,
        ra_roughness=ra_roughness_cls,
        rz_roughness=rz_roughness_cls,
        rq_roughness=rq_roughness_cls,
        rsm_roughness=rsm_roughness_cls,
        enable_generic_erosion_model=enable_generic_erosion_model_cls,
        generic_impact_angle_function=generic_impact_angle_function_cls,
        generic_diameter_function=generic_diameter_function_cls,
        generic_velocity_exponent_function=generic_velocity_exponent_function_cls,
        enable_finnie_erosion_model=enable_finnie_erosion_model_cls,
        dpm_bc_erosion_finnie_k=dpm_bc_erosion_finnie_k_cls,
        dpm_bc_erosion_finnie_vel_exp=dpm_bc_erosion_finnie_vel_exp_cls,
        dpm_bc_erosion_finnie_max_erosion_angle=dpm_bc_erosion_finnie_max_erosion_angle_cls,
        dpm_bc_erosion_mclaury=dpm_bc_erosion_mclaury_cls,
        dpm_bc_erosion_mclaury_a=dpm_bc_erosion_mclaury_a_cls,
        dpm_bc_erosion_mclaury_vel_exp=dpm_bc_erosion_mclaury_vel_exp_cls,
        dpm_bc_erosion_mclaury_transition_angle=dpm_bc_erosion_mclaury_transition_angle_cls,
        dpm_bc_erosion_mclaury_b=dpm_bc_erosion_mclaury_b_cls,
        dpm_bc_erosion_mclaury_c=dpm_bc_erosion_mclaury_c_cls,
        dpm_bc_erosion_mclaury_w=dpm_bc_erosion_mclaury_w_cls,
        dpm_bc_erosion_mclaury_x=dpm_bc_erosion_mclaury_x_cls,
        dpm_bc_erosion_mclaury_y=dpm_bc_erosion_mclaury_y_cls,
        dpm_bc_erosion_oka=dpm_bc_erosion_oka_cls,
        dpm_bc_erosion_oka_e90=dpm_bc_erosion_oka_e90_cls,
        dpm_bc_erosion_oka_hv=dpm_bc_erosion_oka_hv_cls,
        dpm_bc_erosion_oka_n1=dpm_bc_erosion_oka_n1_cls,
        dpm_bc_erosion_oka_n2=dpm_bc_erosion_oka_n2_cls,
        dpm_bc_erosion_oka_k2=dpm_bc_erosion_oka_k2_cls,
        dpm_bc_erosion_oka_k3=dpm_bc_erosion_oka_k3_cls,
        dpm_bc_erosion_oka_dref=dpm_bc_erosion_oka_dref_cls,
        dpm_bc_erosion_oka_vref=dpm_bc_erosion_oka_vref_cls,
        dpm_bc_erosion_dnv=dpm_bc_erosion_dnv_cls,
        dpm_bc_erosion_dnv_k=dpm_bc_erosion_dnv_k_cls,
        dpm_bc_erosion_dnv_n=dpm_bc_erosion_dnv_n_cls,
        dpm_bc_erosion_dnv_ductile=dpm_bc_erosion_dnv_ductile_cls,
        dpm_bc_erosion_shear=dpm_bc_erosion_shear_cls,
        dpm_bc_erosion_shear_v=dpm_bc_erosion_shear_v_cls,
        dpm_bc_erosion_shear_c=dpm_bc_erosion_shear_c_cls,
        dpm_bc_erosion_shear_packing_limit=dpm_bc_erosion_shear_packing_limit_cls,
        dpm_bc_erosion_shielding=dpm_bc_erosion_shielding_cls,
        dpm_wall_heat_exchange=dpm_wall_heat_exchange_cls,
        dpm_film_condensation=dpm_film_condensation_cls,
        dpm_film_bl_model=dpm_film_bl_model_cls,
        dpm_particle_stripping=dpm_particle_stripping_cls,
        dpm_critical_shear_stress=dpm_critical_shear_stress_cls,
        dpm_film_separation_model=dpm_film_separation_model_cls,
        dpm_critical_we_number=dpm_critical_we_number_cls,
        dpm_film_separation_angle=dpm_film_separation_angle_cls,
        dpm_allow_lwf_to_vof=dpm_allow_lwf_to_vof_cls,
        dpm_allow_vof_to_lwf=dpm_allow_vof_to_lwf_cls,
        dpm_initialize_lwf=dpm_initialize_lwf_cls,
        dpm_initial_height=dpm_initial_height_cls,
        film_velocity=film_velocity_cls,
        dpm_initial_temperature=dpm_initial_temperature_cls,
        dpm_initial_injection=dpm_initial_injection_cls,
        film_parcel_surface_area_density=film_parcel_surface_area_density_cls,
        minimum_number_of_parcels_per_face=minimum_number_of_parcels_per_face_cls,
        in_situ_data_reduction=in_situ_data_reduction_cls,
        data_reduction=data_reduction_cls,
        initialize_lwf_now=initialize_lwf_now_cls,
    )

    _child_aliases = dict(
        dpm_bc_norm_coeff="normal_coefficient",
        dpm_bc_tang_coeff="tangential_coefficient",
        dpm_do_initialize_lwf_now="initialize_lwf_now",
        dpm_bc_collision_partner="dem_collision_partner",
        dpm_bc_erosion="generic_impact_angle_function",
        dpm_bc_erosion_c="generic_diameter_function",
        dpm_bc_erosion_finnie="enable_finnie_erosion_model",
        dpm_bc_erosion_generic="enable_generic_erosion_model",
        dpm_bc_erosion_n="generic_velocity_exponent_function",
        dpm_bc_type="discrete_phase_bc_type",
        dpm_bc_udf="discrete_phase_bc_function",
    )

