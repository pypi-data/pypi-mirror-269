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

from .surfaces_19 import surfaces as surfaces_cls
from .reset_reference_mesh import reset_reference_mesh as reset_reference_mesh_cls
from .overlay_reference import overlay_reference as overlay_reference_cls
from .export_displacements import export_displacements as export_displacements_cls
class history(Group):
    """
    Design tool history menu.
    """

    fluent_name = "history"

    child_names = \
        ['surfaces']

    command_names = \
        ['reset_reference_mesh', 'overlay_reference', 'export_displacements']

    _child_classes = dict(
        surfaces=surfaces_cls,
        reset_reference_mesh=reset_reference_mesh_cls,
        overlay_reference=overlay_reference_cls,
        export_displacements=export_displacements_cls,
    )

