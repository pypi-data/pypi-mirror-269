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

from .file_name_12 import file_name as file_name_cls
class write_polar_dist_func_to_file(Command):
    """
    Write polar distribution function to file.
    
    Parameters
    ----------
        file_name : str
            Name of output CSV file.
    
    """

    fluent_name = "write-polar-dist-func-to-file?"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

