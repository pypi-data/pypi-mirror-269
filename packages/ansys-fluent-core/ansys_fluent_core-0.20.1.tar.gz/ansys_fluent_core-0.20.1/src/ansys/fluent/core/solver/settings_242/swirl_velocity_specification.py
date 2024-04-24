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

from .specify_swirl_velocity import specify_swirl_velocity as specify_swirl_velocity_cls
from .fan_axis import fan_axis as fan_axis_cls
from .fan_origin_1 import fan_origin as fan_origin_cls
from .fan_hub_radius import fan_hub_radius as fan_hub_radius_cls
from .profile_specification_of_tangential_velocity import profile_specification_of_tangential_velocity as profile_specification_of_tangential_velocity_cls
from .tangential_velocity_profile import tangential_velocity_profile as tangential_velocity_profile_cls
from .tangential_velocity_polynomial_coeff import tangential_velocity_polynomial_coeff as tangential_velocity_polynomial_coeff_cls
from .profile_specification_of_radial_velocity import profile_specification_of_radial_velocity as profile_specification_of_radial_velocity_cls
from .radial_velocity_profile import radial_velocity_profile as radial_velocity_profile_cls
from .radial_velocity_polynomial_coeff import radial_velocity_polynomial_coeff as radial_velocity_polynomial_coeff_cls
from .swirl_factor import swirl_factor as swirl_factor_cls
class swirl_velocity_specification(Group):
    """
    Swirl Velocity specification settings.
    """

    fluent_name = "swirl-velocity-specification"

    child_names = \
        ['specify_swirl_velocity', 'fan_axis', 'fan_origin', 'fan_hub_radius',
         'profile_specification_of_tangential_velocity',
         'tangential_velocity_profile',
         'tangential_velocity_polynomial_coeff',
         'profile_specification_of_radial_velocity',
         'radial_velocity_profile', 'radial_velocity_polynomial_coeff',
         'swirl_factor']

    _child_classes = dict(
        specify_swirl_velocity=specify_swirl_velocity_cls,
        fan_axis=fan_axis_cls,
        fan_origin=fan_origin_cls,
        fan_hub_radius=fan_hub_radius_cls,
        profile_specification_of_tangential_velocity=profile_specification_of_tangential_velocity_cls,
        tangential_velocity_profile=tangential_velocity_profile_cls,
        tangential_velocity_polynomial_coeff=tangential_velocity_polynomial_coeff_cls,
        profile_specification_of_radial_velocity=profile_specification_of_radial_velocity_cls,
        radial_velocity_profile=radial_velocity_profile_cls,
        radial_velocity_polynomial_coeff=radial_velocity_polynomial_coeff_cls,
        swirl_factor=swirl_factor_cls,
    )

    _child_aliases = dict(
        axis_direction_component="fan_axis",
        axis_origin_component="fan_origin",
        fan_vr="radial_velocity_polynomial_coeff",
        fr="tangential_velocity_polynomial_coeff",
        hub="fan_hub_radius",
        profile_vr="profile_specification_of_radial_velocity",
        profile_vt="profile_specification_of_tangential_velocity",
        swirl_model="specify_swirl_velocity",
        vr_profile="radial_velocity_profile",
        vt_profile="tangential_velocity_profile",
    )

