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
from .surface_name_list import surface_name_list as surface_name_list_cls
from .delimiter import delimiter as delimiter_cls
from .cell_func_domain import cell_func_domain as cell_func_domain_cls
from .location import location as location_cls
class ascii(Command):
    """
    Write an ASCII file.
    
    Parameters
    ----------
        file_name : str
            Enter the desired file name to export.
        surface_name_list : typing.List[str]
            List of surfaces to export.
        delimiter : str
            Select the delimiter separating the fields.
        cell_func_domain : typing.List[str]
            Select the list of quantities to export.
        location : str
            Select the node or cell-center to export data values.
    
    """

    fluent_name = "ascii"

    argument_names = \
        ['file_name', 'surface_name_list', 'delimiter', 'cell_func_domain',
         'location']

    _child_classes = dict(
        file_name=file_name_cls,
        surface_name_list=surface_name_list_cls,
        delimiter=delimiter_cls,
        cell_func_domain=cell_func_domain_cls,
        location=location_cls,
    )

