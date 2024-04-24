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

from .method_19 import method as method_cls
from .frequency_6 import frequency as frequency_cls
from .sampling_after import sampling_after as sampling_after_cls
class evaluation(Group):
    """
    Optimizer observable evaluation settings menu.
    """

    fluent_name = "evaluation"

    child_names = \
        ['method', 'frequency', 'sampling_after']

    _child_classes = dict(
        method=method_cls,
        frequency=frequency_cls,
        sampling_after=sampling_after_cls,
    )

