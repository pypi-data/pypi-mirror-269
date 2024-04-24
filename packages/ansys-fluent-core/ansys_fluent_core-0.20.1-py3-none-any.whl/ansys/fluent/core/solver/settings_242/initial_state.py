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

from .origin_1 import origin as origin_cls
from .orientation import orientation as orientation_cls
class initial_state(Group):
    """
    Specify properties for the initial state of the reference frame.
    """

    fluent_name = "initial-state"

    child_names = \
        ['origin', 'orientation']

    _child_classes = dict(
        origin=origin_cls,
        orientation=orientation_cls,
    )

