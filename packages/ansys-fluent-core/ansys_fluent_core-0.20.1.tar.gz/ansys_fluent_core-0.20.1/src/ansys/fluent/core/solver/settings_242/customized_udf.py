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

from .enabled_32 import enabled as enabled_cls
from .source_file import source_file as source_file_cls
from .create_customized_addon_lib import create_customized_addon_lib as create_customized_addon_lib_cls
from .copy_user_source_file import copy_user_source_file as copy_user_source_file_cls
class customized_udf(Group):
    """
    Enter customized UDFs settings.
    """

    fluent_name = "customized-udf"

    child_names = \
        ['enabled', 'source_file']

    command_names = \
        ['create_customized_addon_lib', 'copy_user_source_file']

    _child_classes = dict(
        enabled=enabled_cls,
        source_file=source_file_cls,
        create_customized_addon_lib=create_customized_addon_lib_cls,
        copy_user_source_file=copy_user_source_file_cls,
    )

