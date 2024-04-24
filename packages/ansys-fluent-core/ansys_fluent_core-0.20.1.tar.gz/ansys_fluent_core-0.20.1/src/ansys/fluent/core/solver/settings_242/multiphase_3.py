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

from .open_channel_1 import open_channel as open_channel_cls
from .inlet_number import inlet_number as inlet_number_cls
from .phase_spec_1 import phase_spec as phase_spec_cls
from .flow_spec import flow_spec as flow_spec_cls
from .free_surface_level import free_surface_level as free_surface_level_cls
from .ht_bottom import ht_bottom as ht_bottom_cls
from .ht_total import ht_total as ht_total_cls
from .vmag import vmag as vmag_cls
from .den_spec import den_spec as den_spec_cls
from .granular_temperature import granular_temperature as granular_temperature_cls
from .interfacial_area_concentration import interfacial_area_concentration as interfacial_area_concentration_cls
from .level_set_function_flux import level_set_function_flux as level_set_function_flux_cls
from .volume_fraction import volume_fraction as volume_fraction_cls
from .population_balance import population_balance as population_balance_cls
from .relative_humidity import relative_humidity as relative_humidity_cls
from .liquid_mass_fraction import liquid_mass_fraction as liquid_mass_fraction_cls
from .log10_droplets_per_unit_volume import log10_droplets_per_unit_volume as log10_droplets_per_unit_volume_cls
class multiphase(Group):
    """
    Help not available.
    """

    fluent_name = "multiphase"

    child_names = \
        ['open_channel', 'inlet_number', 'phase_spec', 'flow_spec',
         'free_surface_level', 'ht_bottom', 'ht_total', 'vmag', 'den_spec',
         'granular_temperature', 'interfacial_area_concentration',
         'level_set_function_flux', 'volume_fraction', 'population_balance',
         'relative_humidity', 'liquid_mass_fraction',
         'log10_droplets_per_unit_volume']

    _child_classes = dict(
        open_channel=open_channel_cls,
        inlet_number=inlet_number_cls,
        phase_spec=phase_spec_cls,
        flow_spec=flow_spec_cls,
        free_surface_level=free_surface_level_cls,
        ht_bottom=ht_bottom_cls,
        ht_total=ht_total_cls,
        vmag=vmag_cls,
        den_spec=den_spec_cls,
        granular_temperature=granular_temperature_cls,
        interfacial_area_concentration=interfacial_area_concentration_cls,
        level_set_function_flux=level_set_function_flux_cls,
        volume_fraction=volume_fraction_cls,
        population_balance=population_balance_cls,
        relative_humidity=relative_humidity_cls,
        liquid_mass_fraction=liquid_mass_fraction_cls,
        log10_droplets_per_unit_volume=log10_droplets_per_unit_volume_cls,
    )

    _child_aliases = dict(
        ht_local="free_surface_level",
        iac="interfacial_area_concentration",
        lsfun="level_set_function_flux",
        wsb="liquid_mass_fraction",
        wsf="relative_humidity",
        wsn="log10_droplets_per_unit_volume",
    )

