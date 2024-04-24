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

from .enabled_9 import enabled as enabled_cls
from .enhanced_formulation_enabled import enhanced_formulation_enabled as enhanced_formulation_enabled_cls
from .constant_during_iterations import constant_during_iterations as constant_during_iterations_cls
from .limiter import limiter as limiter_cls
class linearization(Group):
    """
    Menu containing options to enable/disable linearization of DPM source terms. 
    Please note that source term linearization is only available if the node-based averaging option is not active.
    """

    fluent_name = "linearization"

    child_names = \
        ['enabled', 'enhanced_formulation_enabled',
         'constant_during_iterations', 'limiter']

    _child_classes = dict(
        enabled=enabled_cls,
        enhanced_formulation_enabled=enhanced_formulation_enabled_cls,
        constant_during_iterations=constant_during_iterations_cls,
        limiter=limiter_cls,
    )

    _child_aliases = dict(
        constant_during_flow_iterations="constant_during_iterations",
        enhanced_form_enabled="enhanced_formulation_enabled",
    )

