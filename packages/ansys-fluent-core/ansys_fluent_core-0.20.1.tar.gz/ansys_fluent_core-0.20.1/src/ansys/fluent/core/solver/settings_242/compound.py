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

from .method_17 import method as method_cls
from .conditions_1 import conditions as conditions_cls
class compound(Group):
    """
    Compound conditions menu.
    """

    fluent_name = "compound"

    child_names = \
        ['method', 'conditions']

    _child_classes = dict(
        method=method_cls,
        conditions=conditions_cls,
    )

