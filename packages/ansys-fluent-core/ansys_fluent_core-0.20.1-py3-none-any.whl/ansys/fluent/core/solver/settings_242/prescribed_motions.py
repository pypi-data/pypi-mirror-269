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

from .max_iterations_1 import max_iterations as max_iterations_cls
from .constraint_relaxation import constraint_relaxation as constraint_relaxation_cls
from .preconditioning import preconditioning as preconditioning_cls
class prescribed_motions(Group):
    """
    Prescribed motions menu.
    """

    fluent_name = "prescribed-motions"

    child_names = \
        ['max_iterations', 'constraint_relaxation', 'preconditioning']

    _child_classes = dict(
        max_iterations=max_iterations_cls,
        constraint_relaxation=constraint_relaxation_cls,
        preconditioning=preconditioning_cls,
    )

