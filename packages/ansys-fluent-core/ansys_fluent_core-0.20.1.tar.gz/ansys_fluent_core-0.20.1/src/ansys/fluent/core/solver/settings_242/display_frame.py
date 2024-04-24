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

from .name_4 import name as name_cls
class display_frame(Command):
    """
    To display Reference Frame.
    
    Parameters
    ----------
        name : str
            Display a reference frame by selecting its name.
    
    """

    fluent_name = "display-frame"

    argument_names = \
        ['name']

    _child_classes = dict(
        name=name_cls,
    )

