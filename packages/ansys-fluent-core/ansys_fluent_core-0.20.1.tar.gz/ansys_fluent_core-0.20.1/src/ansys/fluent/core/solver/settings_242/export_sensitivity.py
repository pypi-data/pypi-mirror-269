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

from .file_name_20 import file_name as file_name_cls
class export_sensitivity(Command):
    """
    Write current data sensitivities to file.
    
    Parameters
    ----------
        file_name : str
            Sensitivities file output name.
    
    """

    fluent_name = "export-sensitivity"

    argument_names = \
        ['file_name']

    _child_classes = dict(
        file_name=file_name_cls,
    )

