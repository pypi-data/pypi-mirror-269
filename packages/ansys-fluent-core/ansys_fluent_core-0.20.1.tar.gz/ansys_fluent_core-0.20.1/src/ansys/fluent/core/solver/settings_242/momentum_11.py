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

from .wall_motion import wall_motion as wall_motion_cls
from .moving import moving as moving_cls
from .relative import relative as relative_cls
from .rotating import rotating as rotating_cls
from .components_1 import components as components_cls
from .speed import speed as speed_cls
from .rotation_speed import rotation_speed as rotation_speed_cls
from .rotation_axis_origin import rotation_axis_origin as rotation_axis_origin_cls
from .rotation_axis_direction import rotation_axis_direction as rotation_axis_direction_cls
from .direction_2 import direction as direction_cls
from .velocity_components import velocity_components as velocity_components_cls
from .shear_condition import shear_condition as shear_condition_cls
from .fsi_interface import fsi_interface as fsi_interface_cls
from .periodic_displacement import periodic_displacement as periodic_displacement_cls
from .periodic_imaginary_displacement import periodic_imaginary_displacement as periodic_imaginary_displacement_cls
from .frequency import frequency as frequency_cls
from .amplitude_1 import amplitude as amplitude_cls
from .nodal_diam import nodal_diam as nodal_diam_cls
from .passage_number import passage_number as passage_number_cls
from .fwd import fwd as fwd_cls
from .aero import aero as aero_cls
from .cmplx import cmplx as cmplx_cls
from .norm import norm as norm_cls
from .method_6 import method as method_cls
from .shear_stress import shear_stress as shear_stress_cls
from .fslip import fslip as fslip_cls
from .eslip import eslip as eslip_cls
from .surface_tension_gradient import surface_tension_gradient as surface_tension_gradient_cls
from .specified_shear import specified_shear as specified_shear_cls
from .specularity_coeff import specularity_coeff as specularity_coeff_cls
from .mom_accommodation_coeff import mom_accommodation_coeff as mom_accommodation_coeff_cls
class momentum(Group):
    """
    Help not available.
    """

    fluent_name = "momentum"

    child_names = \
        ['wall_motion', 'moving', 'relative', 'rotating', 'components',
         'speed', 'rotation_speed', 'rotation_axis_origin',
         'rotation_axis_direction', 'direction', 'velocity_components',
         'shear_condition', 'fsi_interface', 'periodic_displacement',
         'periodic_imaginary_displacement', 'frequency', 'amplitude',
         'nodal_diam', 'passage_number', 'fwd', 'aero', 'cmplx', 'norm',
         'method', 'shear_stress', 'fslip', 'eslip',
         'surface_tension_gradient', 'specified_shear', 'specularity_coeff',
         'mom_accommodation_coeff']

    _child_classes = dict(
        wall_motion=wall_motion_cls,
        moving=moving_cls,
        relative=relative_cls,
        rotating=rotating_cls,
        components=components_cls,
        speed=speed_cls,
        rotation_speed=rotation_speed_cls,
        rotation_axis_origin=rotation_axis_origin_cls,
        rotation_axis_direction=rotation_axis_direction_cls,
        direction=direction_cls,
        velocity_components=velocity_components_cls,
        shear_condition=shear_condition_cls,
        fsi_interface=fsi_interface_cls,
        periodic_displacement=periodic_displacement_cls,
        periodic_imaginary_displacement=periodic_imaginary_displacement_cls,
        frequency=frequency_cls,
        amplitude=amplitude_cls,
        nodal_diam=nodal_diam_cls,
        passage_number=passage_number_cls,
        fwd=fwd_cls,
        aero=aero_cls,
        cmplx=cmplx_cls,
        norm=norm_cls,
        method=method_cls,
        shear_stress=shear_stress_cls,
        fslip=fslip_cls,
        eslip=eslip_cls,
        surface_tension_gradient=surface_tension_gradient_cls,
        specified_shear=specified_shear_cls,
        specularity_coeff=specularity_coeff_cls,
        mom_accommodation_coeff=mom_accommodation_coeff_cls,
    )

    _child_aliases = dict(
        amp="amplitude",
        direction_component_of_rotation_axis="rotation_axis_direction",
        freq="frequency",
        mom_accom_coef="mom_accommodation_coeff",
        motion_bc="wall_motion",
        omega="rotation_speed",
        pass_number="passage_number",
        periodic_displacement_components="periodic_displacement",
        periodic_imaginary_displacement_components="periodic_imaginary_displacement",
        position_of_rotation_axis="rotation_axis_origin",
        shear_bc="shear_condition",
        shear_stress_components="shear_stress",
        specular_coeff="specularity_coeff",
        surf_tens_grad="surface_tension_gradient",
        vmag="speed",
        wall_translation_vector="direction",
    )

