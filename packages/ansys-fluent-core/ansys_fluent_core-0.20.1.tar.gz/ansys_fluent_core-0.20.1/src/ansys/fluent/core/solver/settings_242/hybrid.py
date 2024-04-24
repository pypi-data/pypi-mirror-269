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

from .ordered_accumulation import ordered_accumulation as ordered_accumulation_cls
from .dpm_domain import dpm_domain as dpm_domain_cls
class hybrid(Group):
    """
    Main menu to allow users to set options controlling the hybrid parallel scheme used when tracking particles. 
    For more details please consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "hybrid"

    child_names = \
        ['ordered_accumulation', 'dpm_domain']

    _child_classes = dict(
        ordered_accumulation=ordered_accumulation_cls,
        dpm_domain=dpm_domain_cls,
    )

