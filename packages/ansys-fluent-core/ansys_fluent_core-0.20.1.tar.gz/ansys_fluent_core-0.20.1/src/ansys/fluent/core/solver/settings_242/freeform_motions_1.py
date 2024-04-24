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

from .mask_shape_sensitivity import mask_shape_sensitivity as mask_shape_sensitivity_cls
from .solving_primary_morpher import solving_primary_morpher as solving_primary_morpher_cls
from .kernel_type import kernel_type as kernel_type_cls
from .max_iterations_2 import max_iterations as max_iterations_cls
from .linear_solver import linear_solver as linear_solver_cls
class freeform_motions(Group):
    """
    Freeform motions menu.
    """

    fluent_name = "freeform-motions"

    child_names = \
        ['mask_shape_sensitivity', 'solving_primary_morpher', 'kernel_type',
         'max_iterations', 'linear_solver']

    _child_classes = dict(
        mask_shape_sensitivity=mask_shape_sensitivity_cls,
        solving_primary_morpher=solving_primary_morpher_cls,
        kernel_type=kernel_type_cls,
        max_iterations=max_iterations_cls,
        linear_solver=linear_solver_cls,
    )

