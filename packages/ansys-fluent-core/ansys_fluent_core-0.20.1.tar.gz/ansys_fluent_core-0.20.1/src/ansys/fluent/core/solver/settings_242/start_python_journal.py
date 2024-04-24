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

from .file_name_3 import file_name as file_name_cls
class start_python_journal(Command):
    """
    Start recording all input in a python file.
    
    Parameters
    ----------
        file_name : str
            Name of the Python journal file to write.
    
    """

    fluent_name = "start-python-journal"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

