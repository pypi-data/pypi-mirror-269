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

from .file_type import file_type as file_type_cls
from .file_name_1_1 import file_name_1 as file_name_1_cls
class read(Command):
    """
    Allows you to select the file type and import the file.
    
    Parameters
    ----------
        file_type : str
            Select the file type.
        file_name_1 : str
            Specify the name of the file to be read.
    
    """

    fluent_name = "read"

    argument_names = \
        ['file_type', 'file_name']

    _child_classes = dict(
        file_type=file_type_cls,
        file_name=file_name_1_cls,
    )

