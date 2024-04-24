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

from .freeform_motions_1 import freeform_motions as freeform_motions_cls
from .constraint_settings import constraint_settings as constraint_settings_cls
class rbf(Group):
    """
    Design tool RBF numerics menu.
    """

    fluent_name = "rbf"

    child_names = \
        ['freeform_motions', 'constraint_settings']

    _child_classes = dict(
        freeform_motions=freeform_motions_cls,
        constraint_settings=constraint_settings_cls,
    )

