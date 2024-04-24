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

from .max_num_steps import max_num_steps as max_num_steps_cls
from .step_size_controls import step_size_controls as step_size_controls_cls
from .expert_1 import expert as expert_cls
class tracking(Group):
    """
    Main menu to control the time integration of the particle trajectory equations.
    """

    fluent_name = "tracking"

    child_names = \
        ['max_num_steps', 'step_size_controls', 'expert']

    _child_classes = dict(
        max_num_steps=max_num_steps_cls,
        step_size_controls=step_size_controls_cls,
        expert=expert_cls,
    )

    _child_aliases = dict(
        high_res_tracking="__/numerics/high_res_tracking",
        track_in_absolute_frame_enabled="expert/reference_frame",
    )

