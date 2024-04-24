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

from .surface_6 import surface as surface_cls
from .priority import priority as priority_cls
class set_rendering_priority(Command):
    """
    Set the surface rendering priority.
    
    Parameters
    ----------
        surface : str
            Select the surface(s) for surface rendering priority.
        priority : str
            Select the desired rendering priority.
    
    """

    fluent_name = "set-rendering-priority"

    argument_names = \
        ['surface', 'priority']

    _child_classes = dict(
        surface=surface_cls,
        priority=priority_cls,
    )

