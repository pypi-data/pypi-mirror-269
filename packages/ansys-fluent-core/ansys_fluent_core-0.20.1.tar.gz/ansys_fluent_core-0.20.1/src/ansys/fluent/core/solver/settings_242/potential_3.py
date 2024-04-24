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

from .potential_boundary_condition import potential_boundary_condition as potential_boundary_condition_cls
from .potential_boundary_value import potential_boundary_value as potential_boundary_value_cls
from .elec_potential_jump import elec_potential_jump as elec_potential_jump_cls
from .elec_potential_resistance import elec_potential_resistance as elec_potential_resistance_cls
from .electrolyte_potential_boundary_condition import electrolyte_potential_boundary_condition as electrolyte_potential_boundary_condition_cls
from .current_density_boundary_value import current_density_boundary_value as current_density_boundary_value_cls
from .echem_reaction import echem_reaction as echem_reaction_cls
from .elec_potential_mechs import elec_potential_mechs as elec_potential_mechs_cls
from .faradaic_heat import faradaic_heat as faradaic_heat_cls
from .lithium_conc_cond import lithium_conc_cond as lithium_conc_cond_cls
from .lithium_boundary_value import lithium_boundary_value as lithium_boundary_value_cls
class potential(Group):
    """
    Help not available.
    """

    fluent_name = "potential"

    child_names = \
        ['potential_boundary_condition', 'potential_boundary_value',
         'elec_potential_jump', 'elec_potential_resistance',
         'electrolyte_potential_boundary_condition',
         'current_density_boundary_value', 'echem_reaction',
         'elec_potential_mechs', 'faradaic_heat', 'lithium_conc_cond',
         'lithium_boundary_value']

    _child_classes = dict(
        potential_boundary_condition=potential_boundary_condition_cls,
        potential_boundary_value=potential_boundary_value_cls,
        elec_potential_jump=elec_potential_jump_cls,
        elec_potential_resistance=elec_potential_resistance_cls,
        electrolyte_potential_boundary_condition=electrolyte_potential_boundary_condition_cls,
        current_density_boundary_value=current_density_boundary_value_cls,
        echem_reaction=echem_reaction_cls,
        elec_potential_mechs=elec_potential_mechs_cls,
        faradaic_heat=faradaic_heat_cls,
        lithium_conc_cond=lithium_conc_cond_cls,
        lithium_boundary_value=lithium_boundary_value_cls,
    )

    _child_aliases = dict(
        dual_potential_type="electrolyte_potential_boundary_condition",
        dual_potential_value="current_density_boundary_value",
        elec_potential_type="potential_boundary_condition",
        elec_potential_value="potential_boundary_value",
        li_ion_type="lithium_conc_cond",
        li_ion_value="lithium_boundary_value",
    )

