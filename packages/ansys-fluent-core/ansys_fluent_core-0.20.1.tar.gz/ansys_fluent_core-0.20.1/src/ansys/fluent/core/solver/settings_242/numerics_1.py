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

from .polynomials import polynomials as polynomials_cls
from .rbf import rbf as rbf_cls
from .direct_interpolation import direct_interpolation as direct_interpolation_cls
from .default_5 import default as default_cls
class numerics(Group):
    """
    Design tool numerics menu.
    """

    fluent_name = "numerics"

    child_names = \
        ['polynomials', 'rbf', 'direct_interpolation']

    command_names = \
        ['default']

    _child_classes = dict(
        polynomials=polynomials_cls,
        rbf=rbf_cls,
        direct_interpolation=direct_interpolation_cls,
        default=default_cls,
    )

