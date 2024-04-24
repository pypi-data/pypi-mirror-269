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

from .mean_mixture_fraction import mean_mixture_fraction as mean_mixture_fraction_cls
from .secondary_mean_mixture_fraction import secondary_mean_mixture_fraction as secondary_mean_mixture_fraction_cls
from .mixture_fraction_variance import mixture_fraction_variance as mixture_fraction_variance_cls
from .secondary_mixture_fraction_variance import secondary_mixture_fraction_variance as secondary_mixture_fraction_variance_cls
from .specify_species_in_mole_fractions import specify_species_in_mole_fractions as specify_species_in_mole_fractions_cls
from .backflow_species_mass_fraction import backflow_species_mass_fraction as backflow_species_mass_fraction_cls
from .species_mole_fraction import species_mole_fraction as species_mole_fraction_cls
from .backflow_mixture_fraction import backflow_mixture_fraction as backflow_mixture_fraction_cls
from .backflow_mode_2_probability import backflow_mode_2_probability as backflow_mode_2_probability_cls
from .backflow_mode_3_probability import backflow_mode_3_probability as backflow_mode_3_probability_cls
from .backflow_progress_variable import backflow_progress_variable as backflow_progress_variable_cls
from .backflow_progress_variable_variance import backflow_progress_variable_variance as backflow_progress_variable_variance_cls
from .backflow_flame_area_density import backflow_flame_area_density as backflow_flame_area_density_cls
from .backflow_inert_stream import backflow_inert_stream as backflow_inert_stream_cls
from .backflow_pollutant_no_mass_fraction import backflow_pollutant_no_mass_fraction as backflow_pollutant_no_mass_fraction_cls
from .backflow_pollutant_hcn_mass_fraction import backflow_pollutant_hcn_mass_fraction as backflow_pollutant_hcn_mass_fraction_cls
from .backflow_pollutant_nh3_mass_fraction import backflow_pollutant_nh3_mass_fraction as backflow_pollutant_nh3_mass_fraction_cls
from .backflow_pollutant_n2o_mass_fraction import backflow_pollutant_n2o_mass_fraction as backflow_pollutant_n2o_mass_fraction_cls
from .backflow_pollutant_urea_mass_fraction import backflow_pollutant_urea_mass_fraction as backflow_pollutant_urea_mass_fraction_cls
from .backflow_pollutant_hnco_mass_fraction import backflow_pollutant_hnco_mass_fraction as backflow_pollutant_hnco_mass_fraction_cls
from .backflow_pollutant_nco_mass_fraction import backflow_pollutant_nco_mass_fraction as backflow_pollutant_nco_mass_fraction_cls
from .backflow_pollutant_so2_mass_fraction import backflow_pollutant_so2_mass_fraction as backflow_pollutant_so2_mass_fraction_cls
from .backflow_pollutant_h2s_mass_fraction import backflow_pollutant_h2s_mass_fraction as backflow_pollutant_h2s_mass_fraction_cls
from .backflow_pollutant_so3_mass_fraction import backflow_pollutant_so3_mass_fraction as backflow_pollutant_so3_mass_fraction_cls
from .backflow_pollutant_sh_mass_fraction import backflow_pollutant_sh_mass_fraction as backflow_pollutant_sh_mass_fraction_cls
from .backflow_pollutant_so_mass_fraction import backflow_pollutant_so_mass_fraction as backflow_pollutant_so_mass_fraction_cls
from .backflow_soot_mass_fraction import backflow_soot_mass_fraction as backflow_soot_mass_fraction_cls
from .backflow_nuclei import backflow_nuclei as backflow_nuclei_cls
from .backflow_tar_mass_fraction import backflow_tar_mass_fraction as backflow_tar_mass_fraction_cls
from .backflow_pollutant_hg_mass_fraction import backflow_pollutant_hg_mass_fraction as backflow_pollutant_hg_mass_fraction_cls
from .backflow_pollutant_hgcl2_mass_fraction import backflow_pollutant_hgcl2_mass_fraction as backflow_pollutant_hgcl2_mass_fraction_cls
from .backflow_pollutant_hcl_mass_fraction import backflow_pollutant_hcl_mass_fraction as backflow_pollutant_hcl_mass_fraction_cls
from .backflow_pollutant_hgo_mass_fraction import backflow_pollutant_hgo_mass_fraction as backflow_pollutant_hgo_mass_fraction_cls
from .backflow_pollutant_cl_mass_fraction import backflow_pollutant_cl_mass_fraction as backflow_pollutant_cl_mass_fraction_cls
from .backflow_pollutant_cl2_mass_fraction import backflow_pollutant_cl2_mass_fraction as backflow_pollutant_cl2_mass_fraction_cls
from .backflow_pollutant_hgcl_mass_fraction import backflow_pollutant_hgcl_mass_fraction as backflow_pollutant_hgcl_mass_fraction_cls
from .backflow_pollutant_hocl_mass_fraction import backflow_pollutant_hocl_mass_fraction as backflow_pollutant_hocl_mass_fraction_cls
from .tss_scalar import tss_scalar as tss_scalar_cls
class species(Group):
    """
    Help not available.
    """

    fluent_name = "species"

    child_names = \
        ['mean_mixture_fraction', 'secondary_mean_mixture_fraction',
         'mixture_fraction_variance', 'secondary_mixture_fraction_variance',
         'specify_species_in_mole_fractions',
         'backflow_species_mass_fraction', 'species_mole_fraction',
         'backflow_mixture_fraction', 'backflow_mode_2_probability',
         'backflow_mode_3_probability', 'backflow_progress_variable',
         'backflow_progress_variable_variance', 'backflow_flame_area_density',
         'backflow_inert_stream', 'backflow_pollutant_no_mass_fraction',
         'backflow_pollutant_hcn_mass_fraction',
         'backflow_pollutant_nh3_mass_fraction',
         'backflow_pollutant_n2o_mass_fraction',
         'backflow_pollutant_urea_mass_fraction',
         'backflow_pollutant_hnco_mass_fraction',
         'backflow_pollutant_nco_mass_fraction',
         'backflow_pollutant_so2_mass_fraction',
         'backflow_pollutant_h2s_mass_fraction',
         'backflow_pollutant_so3_mass_fraction',
         'backflow_pollutant_sh_mass_fraction',
         'backflow_pollutant_so_mass_fraction', 'backflow_soot_mass_fraction',
         'backflow_nuclei', 'backflow_tar_mass_fraction',
         'backflow_pollutant_hg_mass_fraction',
         'backflow_pollutant_hgcl2_mass_fraction',
         'backflow_pollutant_hcl_mass_fraction',
         'backflow_pollutant_hgo_mass_fraction',
         'backflow_pollutant_cl_mass_fraction',
         'backflow_pollutant_cl2_mass_fraction',
         'backflow_pollutant_hgcl_mass_fraction',
         'backflow_pollutant_hocl_mass_fraction', 'tss_scalar']

    _child_classes = dict(
        mean_mixture_fraction=mean_mixture_fraction_cls,
        secondary_mean_mixture_fraction=secondary_mean_mixture_fraction_cls,
        mixture_fraction_variance=mixture_fraction_variance_cls,
        secondary_mixture_fraction_variance=secondary_mixture_fraction_variance_cls,
        specify_species_in_mole_fractions=specify_species_in_mole_fractions_cls,
        backflow_species_mass_fraction=backflow_species_mass_fraction_cls,
        species_mole_fraction=species_mole_fraction_cls,
        backflow_mixture_fraction=backflow_mixture_fraction_cls,
        backflow_mode_2_probability=backflow_mode_2_probability_cls,
        backflow_mode_3_probability=backflow_mode_3_probability_cls,
        backflow_progress_variable=backflow_progress_variable_cls,
        backflow_progress_variable_variance=backflow_progress_variable_variance_cls,
        backflow_flame_area_density=backflow_flame_area_density_cls,
        backflow_inert_stream=backflow_inert_stream_cls,
        backflow_pollutant_no_mass_fraction=backflow_pollutant_no_mass_fraction_cls,
        backflow_pollutant_hcn_mass_fraction=backflow_pollutant_hcn_mass_fraction_cls,
        backflow_pollutant_nh3_mass_fraction=backflow_pollutant_nh3_mass_fraction_cls,
        backflow_pollutant_n2o_mass_fraction=backflow_pollutant_n2o_mass_fraction_cls,
        backflow_pollutant_urea_mass_fraction=backflow_pollutant_urea_mass_fraction_cls,
        backflow_pollutant_hnco_mass_fraction=backflow_pollutant_hnco_mass_fraction_cls,
        backflow_pollutant_nco_mass_fraction=backflow_pollutant_nco_mass_fraction_cls,
        backflow_pollutant_so2_mass_fraction=backflow_pollutant_so2_mass_fraction_cls,
        backflow_pollutant_h2s_mass_fraction=backflow_pollutant_h2s_mass_fraction_cls,
        backflow_pollutant_so3_mass_fraction=backflow_pollutant_so3_mass_fraction_cls,
        backflow_pollutant_sh_mass_fraction=backflow_pollutant_sh_mass_fraction_cls,
        backflow_pollutant_so_mass_fraction=backflow_pollutant_so_mass_fraction_cls,
        backflow_soot_mass_fraction=backflow_soot_mass_fraction_cls,
        backflow_nuclei=backflow_nuclei_cls,
        backflow_tar_mass_fraction=backflow_tar_mass_fraction_cls,
        backflow_pollutant_hg_mass_fraction=backflow_pollutant_hg_mass_fraction_cls,
        backflow_pollutant_hgcl2_mass_fraction=backflow_pollutant_hgcl2_mass_fraction_cls,
        backflow_pollutant_hcl_mass_fraction=backflow_pollutant_hcl_mass_fraction_cls,
        backflow_pollutant_hgo_mass_fraction=backflow_pollutant_hgo_mass_fraction_cls,
        backflow_pollutant_cl_mass_fraction=backflow_pollutant_cl_mass_fraction_cls,
        backflow_pollutant_cl2_mass_fraction=backflow_pollutant_cl2_mass_fraction_cls,
        backflow_pollutant_hgcl_mass_fraction=backflow_pollutant_hgcl_mass_fraction_cls,
        backflow_pollutant_hocl_mass_fraction=backflow_pollutant_hocl_mass_fraction_cls,
        tss_scalar=tss_scalar_cls,
    )

    _child_aliases = dict(
        ecfm_sigma="backflow_flame_area_density",
        fmean="mean_mixture_fraction",
        fmean2="secondary_mean_mixture_fraction",
        fvar="mixture_fraction_variance",
        fvar2="secondary_mixture_fraction_variance",
        inert="backflow_inert_stream",
        mf="backflow_species_mass_fraction",
        mole_fraction="species_mole_fraction",
        pollut_cl="backflow_pollutant_cl_mass_fraction",
        pollut_cl2="backflow_pollutant_cl2_mass_fraction",
        pollut_ctar="backflow_tar_mass_fraction",
        pollut_h2s="backflow_pollutant_h2s_mass_fraction",
        pollut_hcl="backflow_pollutant_hcl_mass_fraction",
        pollut_hcn="backflow_pollutant_hcn_mass_fraction",
        pollut_hg="backflow_pollutant_hg_mass_fraction",
        pollut_hgcl="backflow_pollutant_hgcl_mass_fraction",
        pollut_hgcl2="backflow_pollutant_hgcl2_mass_fraction",
        pollut_hgo="backflow_pollutant_hgo_mass_fraction",
        pollut_hnco="backflow_pollutant_hnco_mass_fraction",
        pollut_hocl="backflow_pollutant_hocl_mass_fraction",
        pollut_n2o="backflow_pollutant_n2o_mass_fraction",
        pollut_nco="backflow_pollutant_nco_mass_fraction",
        pollut_nh3="backflow_pollutant_nh3_mass_fraction",
        pollut_no="backflow_pollutant_no_mass_fraction",
        pollut_nuclei="backflow_nuclei",
        pollut_sh="backflow_pollutant_sh_mass_fraction",
        pollut_so="backflow_pollutant_so_mass_fraction",
        pollut_so2="backflow_pollutant_so2_mass_fraction",
        pollut_so3="backflow_pollutant_so3_mass_fraction",
        pollut_soot="backflow_soot_mass_fraction",
        pollut_urea="backflow_pollutant_urea_mass_fraction",
        premixc="backflow_progress_variable",
        premixc_var="backflow_progress_variable_variance",
        prob_mode_1="backflow_mixture_fraction",
        prob_mode_2="backflow_mode_2_probability",
        prob_mode_3="backflow_mode_3_probability",
        species_in_mole_fractions="specify_species_in_mole_fractions",
    )

