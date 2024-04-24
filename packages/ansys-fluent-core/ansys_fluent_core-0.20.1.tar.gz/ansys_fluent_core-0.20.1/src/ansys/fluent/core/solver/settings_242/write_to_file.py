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

from .filename_2_3 import filename_2 as filename_2_cls
class write_to_file(Command):
    """
    Write data to a file.
    
    Parameters
    ----------
        filename_2 : str
            Type in the desired file name to save.
    
    """

    fluent_name = "write-to-file"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_2_cls,
    )

