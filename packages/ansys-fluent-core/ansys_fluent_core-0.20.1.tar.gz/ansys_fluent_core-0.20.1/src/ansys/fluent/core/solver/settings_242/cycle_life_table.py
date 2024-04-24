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

from .interp_method import interp_method as interp_method_cls
from .z_value import z_value as z_value_cls
from .column_number import column_number as column_number_cls
from .row_number import row_number as row_number_cls
from .column_value import column_value as column_value_cls
from .row_value import row_value as row_value_cls
from .table_value import table_value as table_value_cls
from .z_label import z_label as z_label_cls
from .column_label import column_label as column_label_cls
from .row_label import row_label as row_label_cls
from .table_label import table_label as table_label_cls
from .write_table import write_table as write_table_cls
from .read_table import read_table as read_table_cls
from .print_table import print_table as print_table_cls
class cycle_life_table(Group):
    """
    Set cycle life table in the empirical life model.
    """

    fluent_name = "cycle-life-table"

    child_names = \
        ['interp_method', 'z_value', 'column_number', 'row_number',
         'column_value', 'row_value', 'table_value', 'z_label',
         'column_label', 'row_label', 'table_label']

    command_names = \
        ['write_table', 'read_table', 'print_table']

    _child_classes = dict(
        interp_method=interp_method_cls,
        z_value=z_value_cls,
        column_number=column_number_cls,
        row_number=row_number_cls,
        column_value=column_value_cls,
        row_value=row_value_cls,
        table_value=table_value_cls,
        z_label=z_label_cls,
        column_label=column_label_cls,
        row_label=row_label_cls,
        table_label=table_label_cls,
        write_table=write_table_cls,
        read_table=read_table_cls,
        print_table=print_table_cls,
    )

