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

from .list_properties import list_properties as list_properties_cls
from .resize import resize as resize_cls
from .write_table_1 import write_table as write_table_cls
from .read_table_1 import read_table as read_table_cls
from .print_table_1 import print_table as print_table_cls
from .internal_resistance_table_child import internal_resistance_table_child

class limit_current_table(ListObject[internal_resistance_table_child]):
    """
    Current limit table in the NTGK model.
    """

    fluent_name = "limit-current-table"

    command_names = \
        ['list_properties', 'resize', 'write_table', 'read_table',
         'print_table']

    _child_classes = dict(
        list_properties=list_properties_cls,
        resize=resize_cls,
        write_table=write_table_cls,
        read_table=read_table_cls,
        print_table=print_table_cls,
    )

    child_object_type: internal_resistance_table_child = internal_resistance_table_child
    """
    child_object_type of limit_current_table.
    """
