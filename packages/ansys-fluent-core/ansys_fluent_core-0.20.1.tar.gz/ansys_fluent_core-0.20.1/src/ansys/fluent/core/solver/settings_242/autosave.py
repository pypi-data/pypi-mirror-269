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

from .file_name_17 import file_name as file_name_cls
from .frequency_5 import frequency as frequency_cls
from .max_files_1 import max_files as max_files_cls
class autosave(Group):
    """
    Menu for adjoint autosave.
    """

    fluent_name = "autosave"

    child_names = \
        ['file_name', 'frequency', 'max_files']

    _child_classes = dict(
        file_name=file_name_cls,
        frequency=frequency_cls,
        max_files=max_files_cls,
    )

