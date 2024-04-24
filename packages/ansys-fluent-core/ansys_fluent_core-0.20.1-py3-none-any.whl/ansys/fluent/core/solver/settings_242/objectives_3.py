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

from .observables_1 import observables as observables_cls
from .operating_conditions_1 import operating_conditions as operating_conditions_cls
from .objectives_2 import objectives as objectives_cls
class objectives(Group):
    """
    Optimizer objectives.
    """

    fluent_name = "objectives"

    child_names = \
        ['observables', 'operating_conditions', 'objectives']

    _child_classes = dict(
        observables=observables_cls,
        operating_conditions=operating_conditions_cls,
        objectives=objectives_cls,
    )

