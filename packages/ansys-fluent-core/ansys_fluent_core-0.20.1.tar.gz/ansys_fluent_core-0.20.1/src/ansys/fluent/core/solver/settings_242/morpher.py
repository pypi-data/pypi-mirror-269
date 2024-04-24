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

from .method_16 import method as method_cls
from .constraint_method import constraint_method as constraint_method_cls
from .numerics_1 import numerics as numerics_cls
class morpher(Group):
    """
    Design tool morphing menu.
    """

    fluent_name = "morpher"

    child_names = \
        ['method', 'constraint_method', 'numerics']

    _child_classes = dict(
        method=method_cls,
        constraint_method=constraint_method_cls,
        numerics=numerics_cls,
    )

