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

from .copy_from import copy_from as copy_from_cls
from .copy_to import copy_to as copy_to_cls
class copy(Command):
    """
    Create a copy of a report definition.
    
    Parameters
    ----------
        copy_from : str
            Select the report definition to copy.
        copy_to : str
            Write the new name for the copied report definition.
    
    """

    fluent_name = "copy"

    argument_names = \
        ['copy_from', 'copy_to']

    _child_classes = dict(
        copy_from=copy_from_cls,
        copy_to=copy_to_cls,
    )

