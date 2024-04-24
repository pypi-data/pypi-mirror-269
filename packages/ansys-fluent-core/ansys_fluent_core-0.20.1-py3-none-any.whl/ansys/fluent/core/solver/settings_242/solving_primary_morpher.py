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

class solving_primary_morpher(Boolean):
    """
    When enabled, this option specifies the standard morphing method (primary morpher) to calculate an initial approximation for the constraint equations. The radial basis function (secondary morpher) then enforces the design constraint by refining the approximation of the constraint equations.
    """

    fluent_name = "solving-primary-morpher"

