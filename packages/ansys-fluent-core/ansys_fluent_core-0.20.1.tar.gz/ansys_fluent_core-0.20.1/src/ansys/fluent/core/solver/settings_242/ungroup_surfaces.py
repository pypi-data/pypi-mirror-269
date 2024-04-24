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

from .surface_5 import surface as surface_cls
class ungroup_surfaces(Command):
    """
    Ungroup previously-grouped surfaces.
    
    Parameters
    ----------
        surface : str
            Select the surface to ungroup.
    
    """

    fluent_name = "ungroup-surfaces"

    argument_names = \
        ['surface']

    _child_classes = dict(
        surface=surface_cls,
    )

