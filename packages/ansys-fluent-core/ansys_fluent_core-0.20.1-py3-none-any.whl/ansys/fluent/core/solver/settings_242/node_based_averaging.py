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

from .enabled_10 import enabled as enabled_cls
from .source_avg_enabled import source_avg_enabled as source_avg_enabled_cls
from .average_every_step import average_every_step as average_every_step_cls
from .kernel import kernel as kernel_cls
class node_based_averaging(Group):
    """
    Menu containing options to enable/disable node-based averaging of DPM variables and DPM source terms. 
    Please note that node-based averaging functionality is only available if source term linearization is not active.
    """

    fluent_name = "node-based-averaging"

    child_names = \
        ['enabled', 'source_avg_enabled', 'average_every_step', 'kernel']

    _child_classes = dict(
        enabled=enabled_cls,
        source_avg_enabled=source_avg_enabled_cls,
        average_every_step=average_every_step_cls,
        kernel=kernel_cls,
    )

    _child_aliases = dict(
        node_avg_enabled="enabled",
    )

