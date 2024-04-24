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

from .option_9 import option as option_cls
from .hybrid import hybrid as hybrid_cls
from .expert_2 import expert as expert_cls
class parallel(Group):
    """
    Main menu to allow users to set options controlling the parallel scheme used when tracking particles. 
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "parallel"

    child_names = \
        ['option', 'hybrid', 'expert']

    _child_classes = dict(
        option=option_cls,
        hybrid=hybrid_cls,
        expert=expert_cls,
    )

