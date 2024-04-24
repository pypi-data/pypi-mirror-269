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

from .export_sensitivity import export_sensitivity as export_sensitivity_cls
from .import_sensitivity import import_sensitivity as import_sensitivity_cls
from .reload import reload as reload_cls
from .remove import remove as remove_cls
from .reload_all import reload_all as reload_all_cls
from .remove_all import remove_all as remove_all_cls
class manage_data(Group):
    """
    Manage sensitivitity data.
    """

    fluent_name = "manage-data"

    command_names = \
        ['export_sensitivity', 'import_sensitivity', 'reload', 'remove',
         'reload_all', 'remove_all']

    _child_classes = dict(
        export_sensitivity=export_sensitivity_cls,
        import_sensitivity=import_sensitivity_cls,
        reload=reload_cls,
        remove=remove_cls,
        reload_all=reload_all_cls,
        remove_all=remove_all_cls,
    )

