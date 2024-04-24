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

from .volumetric_species import volumetric_species as volumetric_species_cls
from .volumetric import volumetric as volumetric_cls
from .site import site as site_cls
from .solid_1 import solid as solid_cls
from .last_species import last_species as last_species_cls
from .material_2 import material as material_cls
class species(Group):
    """
    Mixture species settings.
    """

    fluent_name = "species"

    child_names = \
        ['volumetric_species', 'volumetric', 'site', 'solid', 'last_species',
         'material']

    _child_classes = dict(
        volumetric_species=volumetric_species_cls,
        volumetric=volumetric_cls,
        site=site_cls,
        solid=solid_cls,
        last_species=last_species_cls,
        material=material_cls,
    )

