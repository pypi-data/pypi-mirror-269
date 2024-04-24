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

from .file_name_19 import file_name as file_name_cls
from .unit import unit as unit_cls
class import_surfaces(Command):
    """
    Read surface meshes.
    
    Parameters
    ----------
        file_name : str
            Path to surface mesh file.
        unit : str
            Unit in which the mesh was created.
    
    """

    fluent_name = "import-surfaces"

    argument_names = \
        ['file_name', 'unit']

    _child_classes = dict(
        file_name=file_name_cls,
        unit=unit_cls,
    )

