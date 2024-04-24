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

from .freeform_motions_2 import freeform_motions as freeform_motions_cls
class direct_interpolation(Group):
    """
    Design tool direct interpolation numerics menu.
    """

    fluent_name = "direct-interpolation"

    child_names = \
        ['freeform_motions']

    _child_classes = dict(
        freeform_motions=freeform_motions_cls,
    )

