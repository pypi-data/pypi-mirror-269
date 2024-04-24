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

from .include_current_data_1 import include_current_data as include_current_data_cls
from .training_data_files import training_data_files as training_data_files_cls
from .export_data import export_data as export_data_cls
from .import_data import import_data as import_data_cls
from .remove_1 import remove as remove_cls
class manage_data(Group):
    """
    Set the training parameters.
    """

    fluent_name = "manage-data"

    child_names = \
        ['include_current_data', 'training_data_files']

    command_names = \
        ['export_data', 'import_data', 'remove']

    _child_classes = dict(
        include_current_data=include_current_data_cls,
        training_data_files=training_data_files_cls,
        export_data=export_data_cls,
        import_data=import_data_cls,
        remove=remove_cls,
    )

