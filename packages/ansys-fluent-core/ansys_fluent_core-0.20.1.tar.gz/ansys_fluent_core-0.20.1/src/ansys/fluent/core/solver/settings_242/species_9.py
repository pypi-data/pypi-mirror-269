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
from .mixture_fraction_variance import mixture_fraction_variance as mixture_fraction_variance_cls
from .secondary_mean_mixture_fraction import secondary_mean_mixture_fraction as secondary_mean_mixture_fraction_cls
from .secondary_mixture_fraction_variance import secondary_mixture_fraction_variance as secondary_mixture_fraction_variance_cls
from .specify_species_in_mole_fractions import specify_species_in_mole_fractions as specify_species_in_mole_fractions_cls
from .species_mass_fraction import species_mass_fraction as species_mass_fraction_cls
from .species_mole_fraction import species_mole_fraction as species_mole_fraction_cls
from .mixture_fraction import mixture_fraction as mixture_fraction_cls
from .mode_2_probability import mode_2_probability as mode_2_probability_cls
from .mode_3_probability import mode_3_probability as mode_3_probability_cls
from .pollutant_no_mass_fraction import pollutant_no_mass_fraction as pollutant_no_mass_fraction_cls
from .pollutant_hcn_mass_fraction import pollutant_hcn_mass_fraction as pollutant_hcn_mass_fraction_cls
from .pollutant_nh3_mass_fraction import pollutant_nh3_mass_fraction as pollutant_nh3_mass_fraction_cls
from .pollutant_n2o_mass_fraction import pollutant_n2o_mass_fraction as pollutant_n2o_mass_fraction_cls
from .pollutant_urea_mass_fraction import pollutant_urea_mass_fraction as pollutant_urea_mass_fraction_cls
from .pollutant_hnco_mass_fraction import pollutant_hnco_mass_fraction as pollutant_hnco_mass_fraction_cls
from .pollutant_nco_mass_fraction import pollutant_nco_mass_fraction as pollutant_nco_mass_fraction_cls
from .pollutant_so2_mass_fraction import pollutant_so2_mass_fraction as pollutant_so2_mass_fraction_cls
from .pollutant_h2s_mass_fraction import pollutant_h2s_mass_fraction as pollutant_h2s_mass_fraction_cls
from .pollutant_so3_mass_fraction import pollutant_so3_mass_fraction as pollutant_so3_mass_fraction_cls
from .pollutant_sh_mass_fraction import pollutant_sh_mass_fraction as pollutant_sh_mass_fraction_cls
from .pollutant_so_mass_fraction import pollutant_so_mass_fraction as pollutant_so_mass_fraction_cls
from .soot_mass_fraction import soot_mass_fraction as soot_mass_fraction_cls
from .nuclei import nuclei as nuclei_cls
from .tar_mass_fraction import tar_mass_fraction as tar_mass_fraction_cls
from .pollutant_hg_mass_fraction import pollutant_hg_mass_fraction as pollutant_hg_mass_fraction_cls
from .pollutant_hgcl2_mass_fraction import pollutant_hgcl2_mass_fraction as pollutant_hgcl2_mass_fraction_cls
from .pollutant_hcl_mass_fraction import pollutant_hcl_mass_fraction as pollutant_hcl_mass_fraction_cls
from .pollutant_hgo_mass_fraction import pollutant_hgo_mass_fraction as pollutant_hgo_mass_fraction_cls
from .pollutant_cl_mass_fraction import pollutant_cl_mass_fraction as pollutant_cl_mass_fraction_cls
from .pollutant_cl2_mass_fraction import pollutant_cl2_mass_fraction as pollutant_cl2_mass_fraction_cls
from .pollutant_hgcl_mass_fraction import pollutant_hgcl_mass_fraction as pollutant_hgcl_mass_fraction_cls
from .pollutant_hocl_mass_fraction import pollutant_hocl_mass_fraction as pollutant_hocl_mass_fraction_cls
class species(Group):
    """
    Help not available.
    """

    fluent_name = "species"

    child_names = \
        ['mean_mixture_fraction', 'mixture_fraction_variance',
         'secondary_mean_mixture_fraction',
         'secondary_mixture_fraction_variance',
         'specify_species_in_mole_fractions', 'species_mass_fraction',
         'species_mole_fraction', 'mixture_fraction', 'mode_2_probability',
         'mode_3_probability', 'pollutant_no_mass_fraction',
         'pollutant_hcn_mass_fraction', 'pollutant_nh3_mass_fraction',
         'pollutant_n2o_mass_fraction', 'pollutant_urea_mass_fraction',
         'pollutant_hnco_mass_fraction', 'pollutant_nco_mass_fraction',
         'pollutant_so2_mass_fraction', 'pollutant_h2s_mass_fraction',
         'pollutant_so3_mass_fraction', 'pollutant_sh_mass_fraction',
         'pollutant_so_mass_fraction', 'soot_mass_fraction', 'nuclei',
         'tar_mass_fraction', 'pollutant_hg_mass_fraction',
         'pollutant_hgcl2_mass_fraction', 'pollutant_hcl_mass_fraction',
         'pollutant_hgo_mass_fraction', 'pollutant_cl_mass_fraction',
         'pollutant_cl2_mass_fraction', 'pollutant_hgcl_mass_fraction',
         'pollutant_hocl_mass_fraction']

    _child_classes = dict(
        mean_mixture_fraction=mean_mixture_fraction_cls,
        mixture_fraction_variance=mixture_fraction_variance_cls,
        secondary_mean_mixture_fraction=secondary_mean_mixture_fraction_cls,
        secondary_mixture_fraction_variance=secondary_mixture_fraction_variance_cls,
        specify_species_in_mole_fractions=specify_species_in_mole_fractions_cls,
        species_mass_fraction=species_mass_fraction_cls,
        species_mole_fraction=species_mole_fraction_cls,
        mixture_fraction=mixture_fraction_cls,
        mode_2_probability=mode_2_probability_cls,
        mode_3_probability=mode_3_probability_cls,
        pollutant_no_mass_fraction=pollutant_no_mass_fraction_cls,
        pollutant_hcn_mass_fraction=pollutant_hcn_mass_fraction_cls,
        pollutant_nh3_mass_fraction=pollutant_nh3_mass_fraction_cls,
        pollutant_n2o_mass_fraction=pollutant_n2o_mass_fraction_cls,
        pollutant_urea_mass_fraction=pollutant_urea_mass_fraction_cls,
        pollutant_hnco_mass_fraction=pollutant_hnco_mass_fraction_cls,
        pollutant_nco_mass_fraction=pollutant_nco_mass_fraction_cls,
        pollutant_so2_mass_fraction=pollutant_so2_mass_fraction_cls,
        pollutant_h2s_mass_fraction=pollutant_h2s_mass_fraction_cls,
        pollutant_so3_mass_fraction=pollutant_so3_mass_fraction_cls,
        pollutant_sh_mass_fraction=pollutant_sh_mass_fraction_cls,
        pollutant_so_mass_fraction=pollutant_so_mass_fraction_cls,
        soot_mass_fraction=soot_mass_fraction_cls,
        nuclei=nuclei_cls,
        tar_mass_fraction=tar_mass_fraction_cls,
        pollutant_hg_mass_fraction=pollutant_hg_mass_fraction_cls,
        pollutant_hgcl2_mass_fraction=pollutant_hgcl2_mass_fraction_cls,
        pollutant_hcl_mass_fraction=pollutant_hcl_mass_fraction_cls,
        pollutant_hgo_mass_fraction=pollutant_hgo_mass_fraction_cls,
        pollutant_cl_mass_fraction=pollutant_cl_mass_fraction_cls,
        pollutant_cl2_mass_fraction=pollutant_cl2_mass_fraction_cls,
        pollutant_hgcl_mass_fraction=pollutant_hgcl_mass_fraction_cls,
        pollutant_hocl_mass_fraction=pollutant_hocl_mass_fraction_cls,
    )

    _child_aliases = dict(
        fmean="mean_mixture_fraction",
        fmean2="secondary_mean_mixture_fraction",
        fvar="mixture_fraction_variance",
        fvar2="secondary_mixture_fraction_variance",
        mf="species_mass_fraction",
        mole_fraction="species_mole_fraction",
        pollut_cl="pollutant_cl_mass_fraction",
        pollut_cl2="pollutant_cl2_mass_fraction",
        pollut_ctar="tar_mass_fraction",
        pollut_h2s="pollutant_h2s_mass_fraction",
        pollut_hcl="pollutant_hcl_mass_fraction",
        pollut_hcn="pollutant_hcn_mass_fraction",
        pollut_hg="pollutant_hg_mass_fraction",
        pollut_hgcl="pollutant_hgcl_mass_fraction",
        pollut_hgcl2="pollutant_hgcl2_mass_fraction",
        pollut_hgo="pollutant_hgo_mass_fraction",
        pollut_hnco="pollutant_hnco_mass_fraction",
        pollut_hocl="pollutant_hocl_mass_fraction",
        pollut_n2o="pollutant_n2o_mass_fraction",
        pollut_nco="pollutant_nco_mass_fraction",
        pollut_nh3="pollutant_nh3_mass_fraction",
        pollut_no="pollutant_no_mass_fraction",
        pollut_nuclei="nuclei",
        pollut_sh="pollutant_sh_mass_fraction",
        pollut_so="pollutant_so_mass_fraction",
        pollut_so2="pollutant_so2_mass_fraction",
        pollut_so3="pollutant_so3_mass_fraction",
        pollut_soot="soot_mass_fraction",
        pollut_urea="pollutant_urea_mass_fraction",
        prob_mode_1="mixture_fraction",
        prob_mode_2="mode_2_probability",
        prob_mode_3="mode_3_probability",
        species_in_mole_fractions="specify_species_in_mole_fractions",
    )

