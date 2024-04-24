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

from .file_list_1 import file_list as file_list_cls
class remove(Command):
    """
    Reload sensitivities from data file.
    
    Parameters
    ----------
        file_list : typing.List[str]
            Sensitivities list to remove.
    
    """

    fluent_name = "remove"

    argument_names = \
        ['file_list']

    _child_classes = dict(
        file_list=file_list_cls,
    )

