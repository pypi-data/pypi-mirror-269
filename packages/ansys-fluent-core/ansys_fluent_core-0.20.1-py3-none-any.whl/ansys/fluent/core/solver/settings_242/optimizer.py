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

from .optimizer_type import optimizer_type as optimizer_type_cls
from .objectives_3 import objectives as objectives_cls
from .optimizer_settings import optimizer_settings as optimizer_settings_cls
from .turbulence_model_design_tool import turbulence_model_design_tool as turbulence_model_design_tool_cls
from .mesh_quality import mesh_quality as mesh_quality_cls
from .calculation_activities_1 import calculation_activities as calculation_activities_cls
from .initialize_4 import initialize as initialize_cls
from .reset_3 import reset as reset_cls
from .optimize import optimize as optimize_cls
from .summarize import summarize as summarize_cls
from .default_9 import default as default_cls
class optimizer(Group):
    """
    Gradient-based optimizer menu.
    """

    fluent_name = "optimizer"

    child_names = \
        ['optimizer_type', 'objectives', 'optimizer_settings',
         'turbulence_model_design_tool', 'mesh_quality',
         'calculation_activities']

    command_names = \
        ['initialize', 'reset', 'optimize', 'summarize', 'default']

    _child_classes = dict(
        optimizer_type=optimizer_type_cls,
        objectives=objectives_cls,
        optimizer_settings=optimizer_settings_cls,
        turbulence_model_design_tool=turbulence_model_design_tool_cls,
        mesh_quality=mesh_quality_cls,
        calculation_activities=calculation_activities_cls,
        initialize=initialize_cls,
        reset=reset_cls,
        optimize=optimize_cls,
        summarize=summarize_cls,
        default=default_cls,
    )

