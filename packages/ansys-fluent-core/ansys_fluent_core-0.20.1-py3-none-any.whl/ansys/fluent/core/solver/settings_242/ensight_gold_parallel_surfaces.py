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
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .cell_function import cell_function as cell_function_cls
class ensight_gold_parallel_surfaces(Command):
    """
    Write EnSight Gold geometry, velocity and scalar files for surfaces. Fluent will write files suitable for EnSight Parallel.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        binary_format : bool
            Choose whether or not to export in binary format.
        surfaces : typing.List[str]
            Select surface.
        cell_centered : bool
            Choose whether or not export the cell center data values.
        cell_function : typing.List[str]
            Select the list of quantities to export.
    
    """

    fluent_name = "ensight-gold-parallel-surfaces"

    argument_names = \
        ['file_name', 'binary_format', 'surfaces', 'cell_centered',
         'cell_function']

    _child_classes = dict(
        file_name=file_name_cls,
        binary_format=binary_format_cls,
        surfaces=surfaces_cls,
        cell_centered=cell_centered_cls,
        cell_function=cell_function_cls,
    )

