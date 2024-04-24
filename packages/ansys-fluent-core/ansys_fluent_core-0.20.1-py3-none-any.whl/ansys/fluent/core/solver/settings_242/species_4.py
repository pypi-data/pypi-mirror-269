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

from .particle_species import particle_species as particle_species_cls
from .particle import particle as particle_cls
from .last_species import last_species as last_species_cls
from .material_3 import material as material_cls
class species(Group):
    """
    'species' child.
    """

    fluent_name = "species"

    child_names = \
        ['particle_species', 'particle', 'last_species', 'material']

    _child_classes = dict(
        particle_species=particle_species_cls,
        particle=particle_cls,
        last_species=last_species_cls,
        material=material_cls,
    )

