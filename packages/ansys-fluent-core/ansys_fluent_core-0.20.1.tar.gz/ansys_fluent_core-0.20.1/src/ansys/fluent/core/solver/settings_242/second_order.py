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

class second_order(Boolean):
    """
    When enabled, the second order radial basis function will be used to provide additional smoothness of the deformation. Note that enabling this option may increase the computation time by a factor of 2 - 4 and increase memory by a factor of 3.
    """

    fluent_name = "second-order"

