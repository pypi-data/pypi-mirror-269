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

from .constraints import constraints as constraints_cls
from .parameters_3 import parameters as parameters_cls
class tolerances(Group):
    """
    Motion tolerances menu.
    """

    fluent_name = "tolerances"

    child_names = \
        ['constraints', 'parameters']

    _child_classes = dict(
        constraints=constraints_cls,
        parameters=parameters_cls,
    )

