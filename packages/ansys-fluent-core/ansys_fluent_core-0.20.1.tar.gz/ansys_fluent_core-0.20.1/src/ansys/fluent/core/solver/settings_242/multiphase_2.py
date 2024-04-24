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

from .open_channel import open_channel as open_channel_cls
from .outlet_group_id import outlet_group_id as outlet_group_id_cls
from .phase_spec import phase_spec as phase_spec_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .bottom_level import bottom_level as bottom_level_cls
from .density_interpolation_method import density_interpolation_method as density_interpolation_method_cls
from .backflow_granular_temperature import backflow_granular_temperature as backflow_granular_temperature_cls
from .backflow_interfacial_area_concentration import backflow_interfacial_area_concentration as backflow_interfacial_area_concentration_cls
from .backflow_level_set_function_flux import backflow_level_set_function_flux as backflow_level_set_function_flux_cls
from .volume_frac_spec_method import volume_frac_spec_method as volume_frac_spec_method_cls
from .backflow_volume_fraction import backflow_volume_fraction as backflow_volume_fraction_cls
from .population_balance import population_balance as population_balance_cls
from .backflow_relative_humidity import backflow_relative_humidity as backflow_relative_humidity_cls
from .backflow_liquid_mass_fraction import backflow_liquid_mass_fraction as backflow_liquid_mass_fraction_cls
from .backflow_log10_droplets_per_unit_volume import backflow_log10_droplets_per_unit_volume as backflow_log10_droplets_per_unit_volume_cls
class multiphase(Group):
    """
    Multiphase settings.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'outlet_group_id', 'phase_spec',
         'free_surface_level', 'bottom_level', 'density_interpolation_method',
         'backflow_granular_temperature',
         'backflow_interfacial_area_concentration',
         'backflow_level_set_function_flux', 'volume_frac_spec_method',
         'backflow_volume_fraction', 'population_balance',
         'backflow_relative_humidity', 'backflow_liquid_mass_fraction',
         'backflow_log10_droplets_per_unit_volume']

    _child_classes = dict(
        open_channel=open_channel_cls,
        outlet_group_id=outlet_group_id_cls,
        phase_spec=phase_spec_cls,
        free_surface_level=free_surface_level_cls,
        bottom_level=bottom_level_cls,
        density_interpolation_method=density_interpolation_method_cls,
        backflow_granular_temperature=backflow_granular_temperature_cls,
        backflow_interfacial_area_concentration=backflow_interfacial_area_concentration_cls,
        backflow_level_set_function_flux=backflow_level_set_function_flux_cls,
        volume_frac_spec_method=volume_frac_spec_method_cls,
        backflow_volume_fraction=backflow_volume_fraction_cls,
        population_balance=population_balance_cls,
        backflow_relative_humidity=backflow_relative_humidity_cls,
        backflow_liquid_mass_fraction=backflow_liquid_mass_fraction_cls,
        backflow_log10_droplets_per_unit_volume=backflow_log10_droplets_per_unit_volume_cls,
    )

    _child_aliases = dict(
        den_spec="density_interpolation_method",
        granular_temperature="backflow_granular_temperature",
        ht_bottom="bottom_level",
        ht_local="free_surface_level",
        iac="backflow_interfacial_area_concentration",
        lsfun="backflow_level_set_function_flux",
        outlet_number="outlet_group_id",
        vof_spec="volume_frac_spec_method",
        volume_fraction="backflow_volume_fraction",
        wsb="backflow_liquid_mass_fraction",
        wsf="backflow_relative_humidity",
        wsn="backflow_log10_droplets_per_unit_volume",
    )

