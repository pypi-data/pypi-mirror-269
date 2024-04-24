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

from .porous_jump_turb_wall_treatment import porous_jump_turb_wall_treatment as porous_jump_turb_wall_treatment_cls
from .reverse_fan_direction import reverse_fan_direction as reverse_fan_direction_cls
from .profile_specification_of_pressure_jump import profile_specification_of_pressure_jump as profile_specification_of_pressure_jump_cls
from .pressure_jump import pressure_jump as pressure_jump_cls
from .pressure_jump_profile import pressure_jump_profile as pressure_jump_profile_cls
from .limit_polynomial_velocity_range import limit_polynomial_velocity_range as limit_polynomial_velocity_range_cls
from .min_velocity import min_velocity as min_velocity_cls
from .max_velocity import max_velocity as max_velocity_cls
from .strength import strength as strength_cls
from .cal_pressure_jump_from_avg_conditions import cal_pressure_jump_from_avg_conditions as cal_pressure_jump_from_avg_conditions_cls
from .discrete_phase_bc_type import discrete_phase_bc_type as discrete_phase_bc_type_cls
from .dem_collision_partner import dem_collision_partner as dem_collision_partner_cls
from .reinj_inj import reinj_inj as reinj_inj_cls
from .discrete_phase_bc_function import discrete_phase_bc_function as discrete_phase_bc_function_cls
from .new_fan_definition import new_fan_definition as new_fan_definition_cls
class pressure_jump_specification(Group):
    """
    Pressure jump specification settings.
    """

    fluent_name = "pressure-jump-specification"

    child_names = \
        ['porous_jump_turb_wall_treatment', 'reverse_fan_direction',
         'profile_specification_of_pressure_jump', 'pressure_jump',
         'pressure_jump_profile', 'limit_polynomial_velocity_range',
         'min_velocity', 'max_velocity', 'strength',
         'cal_pressure_jump_from_avg_conditions', 'discrete_phase_bc_type',
         'dem_collision_partner', 'reinj_inj', 'discrete_phase_bc_function',
         'new_fan_definition']

    _child_classes = dict(
        porous_jump_turb_wall_treatment=porous_jump_turb_wall_treatment_cls,
        reverse_fan_direction=reverse_fan_direction_cls,
        profile_specification_of_pressure_jump=profile_specification_of_pressure_jump_cls,
        pressure_jump=pressure_jump_cls,
        pressure_jump_profile=pressure_jump_profile_cls,
        limit_polynomial_velocity_range=limit_polynomial_velocity_range_cls,
        min_velocity=min_velocity_cls,
        max_velocity=max_velocity_cls,
        strength=strength_cls,
        cal_pressure_jump_from_avg_conditions=cal_pressure_jump_from_avg_conditions_cls,
        discrete_phase_bc_type=discrete_phase_bc_type_cls,
        dem_collision_partner=dem_collision_partner_cls,
        reinj_inj=reinj_inj_cls,
        discrete_phase_bc_function=discrete_phase_bc_function_cls,
        new_fan_definition=new_fan_definition_cls,
    )

    _child_aliases = dict(
        average_dp="cal_pressure_jump_from_avg_conditions",
        c="pressure_jump",
        dir="reverse_fan_direction",
        dp_profile="pressure_jump_profile",
        dpm_bc_collision_partner="dem_collision_partner",
        dpm_bc_type_j="discrete_phase_bc_type",
        dpm_bc_udf="discrete_phase_bc_function",
        limit_range="limit_polynomial_velocity_range",
        new_fan_definition="new_fan_definition",
        profile_dp="profile_specification_of_pressure_jump",
        v_max="max_velocity",
        v_min="min_velocity",
    )

