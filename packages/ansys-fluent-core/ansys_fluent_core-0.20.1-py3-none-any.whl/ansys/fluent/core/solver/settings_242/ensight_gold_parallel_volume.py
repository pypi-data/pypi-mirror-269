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

from .file_name_1 import file_name as file_name_cls
from .binary_format import binary_format as binary_format_cls
from .cellzones_1 import cellzones as cellzones_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls
class ensight_gold_parallel_volume(Command):
    """
    Write EnSight Gold geometry, velocity and scalar files for cell zones and boundaries attached to them. Fluent will write files suitable for EnSight Parallel.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        binary_format : bool
            Choose whether or not to export in binary format.
        cellzones : typing.List[str]
            Enter cell zone name list.
        cell_centered : bool
            Choose whether or not export the cell center data values.
        cell_function : typing.List[str]
            Select the list of quantities to export.
    
    """

    fluent_name = "ensight-gold-parallel-volume"

    argument_names = \
        ['file_name', 'binary_format', 'cellzones', 'cell_centered',
         'cell_function']

    _child_classes = dict(
        file_name=file_name_cls,
        binary_format=binary_format_cls,
        cellzones=cellzones_cls,
        cell_centered=cell_centered_cls,
        cell_function=cell_function_cls,
    )

