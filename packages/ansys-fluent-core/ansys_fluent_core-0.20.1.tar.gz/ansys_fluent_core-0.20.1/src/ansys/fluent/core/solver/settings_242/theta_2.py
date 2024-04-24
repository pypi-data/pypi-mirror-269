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

from .points import points as points_cls
from .motion_enabled import motion_enabled as motion_enabled_cls
from .invariant import invariant as invariant_cls
from .invariant_expert_controls import invariant_expert_controls as invariant_expert_controls_cls
from .symmetric import symmetric as symmetric_cls
from .periodicity_1 import periodicity as periodicity_cls
class theta(Group):
    """
    Region conditions in the theta direction.
    """

    fluent_name = "theta"

    child_names = \
        ['points', 'motion_enabled', 'invariant', 'invariant_expert_controls',
         'symmetric', 'periodicity']

    _child_classes = dict(
        points=points_cls,
        motion_enabled=motion_enabled_cls,
        invariant=invariant_cls,
        invariant_expert_controls=invariant_expert_controls_cls,
        symmetric=symmetric_cls,
        periodicity=periodicity_cls,
    )

