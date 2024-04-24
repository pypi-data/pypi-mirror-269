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
from .max_iterations_standard import max_iterations_standard as max_iterations_standard_cls
from .max_iterations_enhanced import max_iterations_enhanced as max_iterations_enhanced_cls
from .constraint_relaxation_1 import constraint_relaxation as constraint_relaxation_cls
from .parameter_relaxation import parameter_relaxation as parameter_relaxation_cls
from .preconditioning_standard import preconditioning_standard as preconditioning_standard_cls
from .preconditioning_enhanced import preconditioning_enhanced as preconditioning_enhanced_cls
class freeform_motions(Group):
    """
    Freeform motions menu.
    """

    fluent_name = "freeform-motions"

    child_names = \
        ['mask_shape_sensitivity', 'solving_primary_morpher',
         'max_iterations_standard', 'max_iterations_enhanced',
         'constraint_relaxation', 'parameter_relaxation',
         'preconditioning_standard', 'preconditioning_enhanced']

    _child_classes = dict(
        mask_shape_sensitivity=mask_shape_sensitivity_cls,
        solving_primary_morpher=solving_primary_morpher_cls,
        max_iterations_standard=max_iterations_standard_cls,
        max_iterations_enhanced=max_iterations_enhanced_cls,
        constraint_relaxation=constraint_relaxation_cls,
        parameter_relaxation=parameter_relaxation_cls,
        preconditioning_standard=preconditioning_standard_cls,
        preconditioning_enhanced=preconditioning_enhanced_cls,
    )

