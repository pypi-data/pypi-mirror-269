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

from .method_20 import method as method_cls
from .current_design_iteration import current_design_iteration as current_design_iteration_cls
from .design_iterations import design_iterations as design_iterations_cls
from .convergence_criteria import convergence_criteria as convergence_criteria_cls
from .flow_iterations import flow_iterations as flow_iterations_cls
from .adjoint_iterations import adjoint_iterations as adjoint_iterations_cls
class optimizer_settings(Group):
    """
    Optimizer settings.
    """

    fluent_name = "optimizer-settings"

    child_names = \
        ['method', 'current_design_iteration', 'design_iterations',
         'convergence_criteria', 'flow_iterations', 'adjoint_iterations']

    _child_classes = dict(
        method=method_cls,
        current_design_iteration=current_design_iteration_cls,
        design_iterations=design_iterations_cls,
        convergence_criteria=convergence_criteria_cls,
        flow_iterations=flow_iterations_cls,
        adjoint_iterations=adjoint_iterations_cls,
    )

