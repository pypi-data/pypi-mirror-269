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
from .scale_7 import scale as scale_cls
from .transparency_2 import transparency as transparency_cls
from .displayed_meshes import displayed_meshes as displayed_meshes_cls
from .outline_1 import outline as outline_cls
from .interior_3 import interior as interior_cls
from .display_10 import display as display_cls
from .export_stl import export_stl as export_stl_cls
class preview(Group):
    """
    Design tool export menu.
    """

    fluent_name = "preview"

    child_names = \
        ['surfaces', 'scale', 'transparency', 'displayed_meshes']

    command_names = \
        ['outline', 'interior', 'display', 'export_stl']

    _child_classes = dict(
        surfaces=surfaces_cls,
        scale=scale_cls,
        transparency=transparency_cls,
        displayed_meshes=displayed_meshes_cls,
        outline=outline_cls,
        interior=interior_cls,
        display=display_cls,
        export_stl=export_stl_cls,
    )

