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

from .surfaces_18 import surfaces as surfaces_cls
from .file_name_25 import file_name as file_name_cls
class stl_surfaces(Command):
    """
    Export specified surfaces from 3D cases as an .stl file.
    
    Parameters
    ----------
        surfaces : typing.List[str]
            Specify surfaces to be exported as .stl file.
        file_name : str
            Export specified surfaces from 3D cases as an .stl file.
    
    """

    fluent_name = "stl-surfaces"

    argument_names = \
        ['surfaces', 'file_name']

    _child_classes = dict(
        surfaces=surfaces_cls,
        file_name=file_name_cls,
    )

