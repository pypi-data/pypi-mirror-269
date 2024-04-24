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

from .bc_type_2 import bc_type as bc_type_cls
from .boundary_source import boundary_source as boundary_source_cls
from .polar_distribution_function import polar_distribution_function as polar_distribution_function_cls
from .polar_func_type import polar_func_type as polar_func_type_cls
from .polar_expression import polar_expression as polar_expression_cls
from .polar_data_pairs import polar_data_pairs as polar_data_pairs_cls
from .beam_width import beam_width as beam_width_cls
from .direct_irradiation import direct_irradiation as direct_irradiation_cls
from .parallel_collimated_beam import parallel_collimated_beam as parallel_collimated_beam_cls
from .reference_direction_1 import reference_direction as reference_direction_cls
from .internal_emissivity import internal_emissivity as internal_emissivity_cls
from .internal_emissivity_band import internal_emissivity_band as internal_emissivity_band_cls
from .diffuse_irradiation_band import diffuse_irradiation_band as diffuse_irradiation_band_cls
from .diffuse_fraction_band import diffuse_fraction_band as diffuse_fraction_band_cls
from .radiating_s2s_surface import radiating_s2s_surface as radiating_s2s_surface_cls
from .critical_zone import critical_zone as critical_zone_cls
from .faces_per_surface_cluster import faces_per_surface_cluster as faces_per_surface_cluster_cls
from .solar_fluxes import solar_fluxes as solar_fluxes_cls
from .solar_direction import solar_direction as solar_direction_cls
from .solar_irradiation import solar_irradiation as solar_irradiation_cls
from .transmissivity import transmissivity as transmissivity_cls
from .absorptivity import absorptivity as absorptivity_cls
from .read_polar_dist_func_from_file import read_polar_dist_func_from_file as read_polar_dist_func_from_file_cls
from .write_polar_dist_func_to_file import write_polar_dist_func_to_file as write_polar_dist_func_to_file_cls
class radiation(Group):
    """
    Radiation settings for this boundary-condition.
    """

    fluent_name = "radiation"

    child_names = \
        ['bc_type', 'boundary_source', 'polar_distribution_function',
         'polar_func_type', 'polar_expression', 'polar_data_pairs',
         'beam_width', 'direct_irradiation', 'parallel_collimated_beam',
         'reference_direction', 'internal_emissivity',
         'internal_emissivity_band', 'diffuse_irradiation_band',
         'diffuse_fraction_band', 'radiating_s2s_surface', 'critical_zone',
         'faces_per_surface_cluster', 'solar_fluxes', 'solar_direction',
         'solar_irradiation', 'transmissivity', 'absorptivity']

    command_names = \
        ['read_polar_dist_func_from_file', 'write_polar_dist_func_to_file']

    _child_classes = dict(
        bc_type=bc_type_cls,
        boundary_source=boundary_source_cls,
        polar_distribution_function=polar_distribution_function_cls,
        polar_func_type=polar_func_type_cls,
        polar_expression=polar_expression_cls,
        polar_data_pairs=polar_data_pairs_cls,
        beam_width=beam_width_cls,
        direct_irradiation=direct_irradiation_cls,
        parallel_collimated_beam=parallel_collimated_beam_cls,
        reference_direction=reference_direction_cls,
        internal_emissivity=internal_emissivity_cls,
        internal_emissivity_band=internal_emissivity_band_cls,
        diffuse_irradiation_band=diffuse_irradiation_band_cls,
        diffuse_fraction_band=diffuse_fraction_band_cls,
        radiating_s2s_surface=radiating_s2s_surface_cls,
        critical_zone=critical_zone_cls,
        faces_per_surface_cluster=faces_per_surface_cluster_cls,
        solar_fluxes=solar_fluxes_cls,
        solar_direction=solar_direction_cls,
        solar_irradiation=solar_irradiation_cls,
        transmissivity=transmissivity_cls,
        absorptivity=absorptivity_cls,
        read_polar_dist_func_from_file=read_polar_dist_func_from_file_cls,
        write_polar_dist_func_to_file=write_polar_dist_func_to_file_cls,
    )

    _child_aliases = dict(
        band_diffuse_frac="diffuse_fraction_band",
        band_in_emiss="internal_emissivity_band",
        band_q_irrad="direct_irradiation",
        band_q_irrad_diffuse="diffuse_irradiation_band",
        component_of_radiation_direction="reference_direction",
        fpsc="faces_per_surface_cluster",
        in_emiss="internal_emissivity",
        mc_bsource_p="boundary_source",
        mc_polar_expr="polar_expression",
        mc_poldfun_p="polar_distribution_function",
        polar_pair_list="polar_data_pairs",
        radiation_bc="bc_type",
    )

