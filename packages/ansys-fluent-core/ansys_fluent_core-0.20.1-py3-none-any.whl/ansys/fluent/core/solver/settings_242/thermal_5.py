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

from .temperature_1 import temperature as temperature_cls
from .thermodynamic_non_equilibrium_boundary import thermodynamic_non_equilibrium_boundary as thermodynamic_non_equilibrium_boundary_cls
from .vibrational_electronic_temperature_1 import vibrational_electronic_temperature as vibrational_electronic_temperature_cls
class thermal(Group):
    """
    Help not available.
    """

    fluent_name = "thermal"

    child_names = \
        ['temperature', 'thermodynamic_non_equilibrium_boundary',
         'vibrational_electronic_temperature']

    _child_classes = dict(
        temperature=temperature_cls,
        thermodynamic_non_equilibrium_boundary=thermodynamic_non_equilibrium_boundary_cls,
        vibrational_electronic_temperature=vibrational_electronic_temperature_cls,
    )

    _child_aliases = dict(
        non_equil_boundary="thermodynamic_non_equilibrium_boundary",
        t="temperature",
        tve="vibrational_electronic_temperature",
    )

