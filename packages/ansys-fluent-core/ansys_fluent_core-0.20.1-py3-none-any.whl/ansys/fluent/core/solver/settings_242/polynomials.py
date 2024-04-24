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

from .auto_select_smoothness import auto_select_smoothness as auto_select_smoothness_cls
from .prescribed_motions import prescribed_motions as prescribed_motions_cls
from .freeform_motions import freeform_motions as freeform_motions_cls
from .constraint_settings import constraint_settings as constraint_settings_cls
from .tolerances import tolerances as tolerances_cls
class polynomials(Group):
    """
    Design tool polynomials numerics menu.
    """

    fluent_name = "polynomials"

    child_names = \
        ['auto_select_smoothness', 'prescribed_motions', 'freeform_motions',
         'constraint_settings', 'tolerances']

    _child_classes = dict(
        auto_select_smoothness=auto_select_smoothness_cls,
        prescribed_motions=prescribed_motions_cls,
        freeform_motions=freeform_motions_cls,
        constraint_settings=constraint_settings_cls,
        tolerances=tolerances_cls,
    )

