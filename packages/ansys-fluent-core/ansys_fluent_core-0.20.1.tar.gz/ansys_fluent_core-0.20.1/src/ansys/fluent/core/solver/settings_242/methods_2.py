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

from .delete_1 import delete as delete_cls
from .rename import rename as rename_cls
from .list import list as list_cls
from .list_properties_1 import list_properties as list_properties_cls
from .make_a_copy import make_a_copy as make_a_copy_cls
from .default_1 import default as default_cls
from .balanced import balanced as balanced_cls
from .best_match import best_match as best_match_cls
from .methods_child import methods_child

class methods(NamedObject[methods_child], _NonCreatableNamedObjectMixin[methods_child]):
    """
    Enter the adjoint solution methods menu.
    """

    fluent_name = "methods"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy',
         'default', 'balanced', 'best_match']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
        default=default_cls,
        balanced=balanced_cls,
        best_match=best_match_cls,
    )

    child_object_type: methods_child = methods_child
    """
    child_object_type of methods.
    """
