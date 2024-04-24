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
from .scope import scope as scope_cls
from .cell_zones import cell_zones as cell_zones_cls
from .surfaces import surfaces as surfaces_cls
from .cell_centered import cell_centered as cell_centered_cls
from .format_class import format_class as format_class_cls
from .cgns_scalar import cgns_scalar as cgns_scalar_cls
class cgns(Command):
    """
    Write a CGNS file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        scope : str
            Select the scope of the export (volume, surface, full domain).
        cell_zones : typing.List[str]
            Enter cell zone name list.
        surfaces : typing.List[str]
            Select surface.
        cell_centered : bool
            Choose whether or not export the cell center data values.
        format_class : str
            Select the format to export.
        cgns_scalar : typing.List[str]
            Select the list of quantities to export.
    
    """

    fluent_name = "cgns"

    argument_names = \
        ['file_name', 'scope', 'cell_zones', 'surfaces', 'cell_centered',
         'format_class', 'cgns_scalar']

    _child_classes = dict(
        file_name=file_name_cls,
        scope=scope_cls,
        cell_zones=cell_zones_cls,
        surfaces=surfaces_cls,
        cell_centered=cell_centered_cls,
        format_class=format_class_cls,
        cgns_scalar=cgns_scalar_cls,
    )

