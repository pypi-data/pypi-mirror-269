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

from .max_iterations_3 import max_iterations as max_iterations_cls
class freeform_motions(Group):
    """
    Freeform motions menu.
    """

    fluent_name = "freeform-motions"

    child_names = \
        ['max_iterations']

    _child_classes = dict(
        max_iterations=max_iterations_cls,
    )

