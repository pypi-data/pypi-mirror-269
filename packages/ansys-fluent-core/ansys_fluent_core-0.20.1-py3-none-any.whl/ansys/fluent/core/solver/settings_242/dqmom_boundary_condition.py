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
from .discrete_boundary_condition_child import discrete_boundary_condition_child

class dqmom_boundary_condition(NamedObject[discrete_boundary_condition_child], _NonCreatableNamedObjectMixin[discrete_boundary_condition_child]):
    """
    List of boundary conditions for DQMOM population balance model.
    """

    fluent_name = "dqmom-boundary-condition"

    command_names = \
        ['delete', 'rename', 'list', 'list_properties', 'make_a_copy']

    _child_classes = dict(
        delete=delete_cls,
        rename=rename_cls,
        list=list_cls,
        list_properties=list_properties_cls,
        make_a_copy=make_a_copy_cls,
    )

    child_object_type: discrete_boundary_condition_child = discrete_boundary_condition_child
    """
    child_object_type of dqmom_boundary_condition.
    """
