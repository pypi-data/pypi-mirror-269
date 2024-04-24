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

from .turbulent_specification import turbulent_specification as turbulent_specification_cls
from .backflow_modified_turbulent_viscosity import backflow_modified_turbulent_viscosity as backflow_modified_turbulent_viscosity_cls
from .backflow_laminar_kinetic_energy import backflow_laminar_kinetic_energy as backflow_laminar_kinetic_energy_cls
from .backflow_intermittency import backflow_intermittency as backflow_intermittency_cls
from .backflow_turbulent_kinetic_energy import backflow_turbulent_kinetic_energy as backflow_turbulent_kinetic_energy_cls
from .backflow_turbulent_dissipation_rate import backflow_turbulent_dissipation_rate as backflow_turbulent_dissipation_rate_cls
from .backflow_specific_dissipation_rate import backflow_specific_dissipation_rate as backflow_specific_dissipation_rate_cls
from .backflow_velocity_variance_scale import backflow_velocity_variance_scale as backflow_velocity_variance_scale_cls
from .backflow_turbulent_intensity import backflow_turbulent_intensity as backflow_turbulent_intensity_cls
from .backflow_turbulent_length_scale import backflow_turbulent_length_scale as backflow_turbulent_length_scale_cls
from .backflow_hydraulic_diameter import backflow_hydraulic_diameter as backflow_hydraulic_diameter_cls
from .backflow_turbulent_viscosity_ratio import backflow_turbulent_viscosity_ratio as backflow_turbulent_viscosity_ratio_cls
from .backflow_turbulent_viscosity_ratio_profile import backflow_turbulent_viscosity_ratio_profile as backflow_turbulent_viscosity_ratio_profile_cls
from .reynolds_stress_specification import reynolds_stress_specification as reynolds_stress_specification_cls
from .backflow_uu_reynolds_stresses import backflow_uu_reynolds_stresses as backflow_uu_reynolds_stresses_cls
from .backflow_vv_reynolds_stresses import backflow_vv_reynolds_stresses as backflow_vv_reynolds_stresses_cls
from .backflow_ww_reynolds_stresses import backflow_ww_reynolds_stresses as backflow_ww_reynolds_stresses_cls
from .backflow_uv_reynolds_stresses import backflow_uv_reynolds_stresses as backflow_uv_reynolds_stresses_cls
from .backflow_vw_reynolds_stresses import backflow_vw_reynolds_stresses as backflow_vw_reynolds_stresses_cls
from .backflow_uw_reynolds_stresses import backflow_uw_reynolds_stresses as backflow_uw_reynolds_stresses_cls
from .subgrid_kinetic_energy_specification import subgrid_kinetic_energy_specification as subgrid_kinetic_energy_specification_cls
from .subgrid_kinetic_energy import subgrid_kinetic_energy as subgrid_kinetic_energy_cls
from .subgrid_turbulent_intensity import subgrid_turbulent_intensity as subgrid_turbulent_intensity_cls
class turbulence(Group):
    """
    Help not available.
    """

    fluent_name = "turbulence"

    child_names = \
        ['turbulent_specification', 'backflow_modified_turbulent_viscosity',
         'backflow_laminar_kinetic_energy', 'backflow_intermittency',
         'backflow_turbulent_kinetic_energy',
         'backflow_turbulent_dissipation_rate',
         'backflow_specific_dissipation_rate',
         'backflow_velocity_variance_scale', 'backflow_turbulent_intensity',
         'backflow_turbulent_length_scale', 'backflow_hydraulic_diameter',
         'backflow_turbulent_viscosity_ratio',
         'backflow_turbulent_viscosity_ratio_profile',
         'reynolds_stress_specification', 'backflow_uu_reynolds_stresses',
         'backflow_vv_reynolds_stresses', 'backflow_ww_reynolds_stresses',
         'backflow_uv_reynolds_stresses', 'backflow_vw_reynolds_stresses',
         'backflow_uw_reynolds_stresses',
         'subgrid_kinetic_energy_specification', 'subgrid_kinetic_energy',
         'subgrid_turbulent_intensity']

    _child_classes = dict(
        turbulent_specification=turbulent_specification_cls,
        backflow_modified_turbulent_viscosity=backflow_modified_turbulent_viscosity_cls,
        backflow_laminar_kinetic_energy=backflow_laminar_kinetic_energy_cls,
        backflow_intermittency=backflow_intermittency_cls,
        backflow_turbulent_kinetic_energy=backflow_turbulent_kinetic_energy_cls,
        backflow_turbulent_dissipation_rate=backflow_turbulent_dissipation_rate_cls,
        backflow_specific_dissipation_rate=backflow_specific_dissipation_rate_cls,
        backflow_velocity_variance_scale=backflow_velocity_variance_scale_cls,
        backflow_turbulent_intensity=backflow_turbulent_intensity_cls,
        backflow_turbulent_length_scale=backflow_turbulent_length_scale_cls,
        backflow_hydraulic_diameter=backflow_hydraulic_diameter_cls,
        backflow_turbulent_viscosity_ratio=backflow_turbulent_viscosity_ratio_cls,
        backflow_turbulent_viscosity_ratio_profile=backflow_turbulent_viscosity_ratio_profile_cls,
        reynolds_stress_specification=reynolds_stress_specification_cls,
        backflow_uu_reynolds_stresses=backflow_uu_reynolds_stresses_cls,
        backflow_vv_reynolds_stresses=backflow_vv_reynolds_stresses_cls,
        backflow_ww_reynolds_stresses=backflow_ww_reynolds_stresses_cls,
        backflow_uv_reynolds_stresses=backflow_uv_reynolds_stresses_cls,
        backflow_vw_reynolds_stresses=backflow_vw_reynolds_stresses_cls,
        backflow_uw_reynolds_stresses=backflow_uw_reynolds_stresses_cls,
        subgrid_kinetic_energy_specification=subgrid_kinetic_energy_specification_cls,
        subgrid_kinetic_energy=subgrid_kinetic_energy_cls,
        subgrid_turbulent_intensity=subgrid_turbulent_intensity_cls,
    )

    _child_aliases = dict(
        e="backflow_turbulent_dissipation_rate",
        hydraulic_diameter="backflow_hydraulic_diameter",
        intermit="backflow_intermittency",
        intermittency="backflow_intermittency",
        k="backflow_turbulent_kinetic_energy",
        kl="backflow_laminar_kinetic_energy",
        ksgs="subgrid_kinetic_energy",
        ksgs_spec="subgrid_kinetic_energy_specification",
        laminar_kinetic_energy="backflow_laminar_kinetic_energy",
        modified_turbulent_viscosity="backflow_modified_turbulent_viscosity",
        nut="backflow_modified_turbulent_viscosity",
        o="backflow_specific_dissipation_rate",
        reynolds_stress_specification="backflow_reynolds_stress_specification",
        rst_spec="reynolds_stress_specification",
        sgs_turb_intensity="subgrid_turbulent_intensity",
        specific_dissipation_rate="backflow_specific_dissipation_rate",
        subgrid_kinetic_energy="backflow_subgrid_kinetic_energy",
        subgrid_kinetic_energy_specification="backflow_subgrid_kinetic_energy_specification",
        subgrid_turbulent_intensity="backflow_subgrid_turbulent_intensity",
        turb_hydraulic_diam="backflow_hydraulic_diameter",
        turb_intensity="backflow_turbulent_intensity",
        turb_length_scale="backflow_turbulent_length_scale",
        turb_viscosity_ratio="backflow_turbulent_viscosity_ratio",
        turb_viscosity_ratio_profile="backflow_turbulent_viscosity_ratio_profile",
        turbulent_dissipation_rate="backflow_turbulent_dissipation_rate",
        turbulent_intensity="backflow_turbulent_intensity",
        turbulent_length_scale="backflow_turbulent_length_scale",
        turbulent_viscosity_ratio="backflow_turbulent_viscosity_ratio",
        turbulent_viscosity_ratio_profile="backflow_turbulent_viscosity_ratio_profile",
        uu="backflow_uu_reynolds_stresses",
        uu_reynolds_stresses="backflow_uu_reynolds_stresses",
        uv="backflow_uv_reynolds_stresses",
        uv_reynolds_stresses="backflow_uv_reynolds_stresses",
        uw="backflow_uw_reynolds_stresses",
        uw_reynolds_stresses="backflow_uw_reynolds_stresses",
        v2="backflow_velocity_variance_scale",
        velocity_variance_scale="backflow_velocity_variance_scale",
        vv="backflow_vv_reynolds_stresses",
        vv_reynolds_stresses="backflow_vv_reynolds_stresses",
        vw="backflow_vw_reynolds_stresses",
        vw_reynolds_stresses="backflow_vw_reynolds_stresses",
        ww="backflow_ww_reynolds_stresses",
        ww_reynolds_stresses="backflow_ww_reynolds_stresses",
    )

