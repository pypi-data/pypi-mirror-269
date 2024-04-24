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

from .selection_3 import selection as selection_cls
from .options_20 import options as options_cls
from .limits_1 import limits as limits_cls
from .default_limits import default_limits as default_limits_cls
from .initialize_3 import initialize as initialize_cls
class design_variables(Group):
    """
    Turbulence model design variables settings.
    """

    fluent_name = "design-variables"

    child_names = \
        ['selection', 'options', 'limits']

    command_names = \
        ['default_limits', 'initialize']

    _child_classes = dict(
        selection=selection_cls,
        options=options_cls,
        limits=limits_cls,
        default_limits=default_limits_cls,
        initialize=initialize_cls,
    )

