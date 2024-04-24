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

from .expected_changes import expected_changes as expected_changes_cls
from .optimal_displacements import optimal_displacements as optimal_displacements_cls
from .stl_surfaces import stl_surfaces as stl_surfaces_cls
class export(Group):
    """
    Design tool export menu.
    """

    fluent_name = "export"

    command_names = \
        ['expected_changes', 'optimal_displacements', 'stl_surfaces']

    _child_classes = dict(
        expected_changes=expected_changes_cls,
        optimal_displacements=optimal_displacements_cls,
        stl_surfaces=stl_surfaces_cls,
    )

