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

from .open_channel_2 import open_channel as open_channel_cls
from .inlet_number import inlet_number as inlet_number_cls
from .secondary_phase_for_inlet import secondary_phase_for_inlet as secondary_phase_for_inlet_cls
from .free_surface_level_1 import free_surface_level as free_surface_level_cls
from .bottom_level_1 import bottom_level as bottom_level_cls
from .density_interpolation_method_1 import density_interpolation_method as density_interpolation_method_cls
from .population_balance import population_balance as population_balance_cls
from .slip_velocity_specification import slip_velocity_specification as slip_velocity_specification_cls
from .phase_velocity_ratio import phase_velocity_ratio as phase_velocity_ratio_cls
from .volume_fraction_1 import volume_fraction as volume_fraction_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration import interfacial_area_concentration as interfacial_area_concentration_cls
from .relative_humidity_1 import relative_humidity as relative_humidity_cls
from .liquid_mass_fraction_1 import liquid_mass_fraction as liquid_mass_fraction_cls
from .log10_droplets_per_unit_volume_1 import log10_droplets_per_unit_volume as log10_droplets_per_unit_volume_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'inlet_number', 'secondary_phase_for_inlet',
         'free_surface_level', 'bottom_level', 'density_interpolation_method',
         'population_balance', 'slip_velocity_specification',
         'phase_velocity_ratio', 'volume_fraction', 'granular_temperature',
         'interfacial_area_concentration', 'relative_humidity',
         'liquid_mass_fraction', 'log10_droplets_per_unit_volume']

    _child_classes = dict(
        open_channel=open_channel_cls,
        inlet_number=inlet_number_cls,
        secondary_phase_for_inlet=secondary_phase_for_inlet_cls,
        free_surface_level=free_surface_level_cls,
        bottom_level=bottom_level_cls,
        density_interpolation_method=density_interpolation_method_cls,
        population_balance=population_balance_cls,
        slip_velocity_specification=slip_velocity_specification_cls,
        phase_velocity_ratio=phase_velocity_ratio_cls,
        volume_fraction=volume_fraction_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        relative_humidity=relative_humidity_cls,
        liquid_mass_fraction=liquid_mass_fraction_cls,
        log10_droplets_per_unit_volume=log10_droplets_per_unit_volume_cls,
    )

    _child_aliases = dict(
        den_spec="density_interpolation_method",
        ht_bottom="bottom_level",
        ht_local="free_surface_level",
        iac="interfacial_area_concentration",
        open_channel="open_channel",
        phase_spec="secondary_phase_for_inlet",
        slip_velocity="slip_velocity_specification",
        velocity_ratio="phase_velocity_ratio",
        volume_frac="volume_fraction",
        wsb="liquid_mass_fraction",
        wsf="relative_humidity",
        wsn="log10_droplets_per_unit_volume",
    )

