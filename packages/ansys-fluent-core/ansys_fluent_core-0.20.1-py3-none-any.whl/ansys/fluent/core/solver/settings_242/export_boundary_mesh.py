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

from .filename_2_1 import filename_2 as filename_2_cls
from .boundary_list_1 import boundary_list as boundary_list_cls
from .global_ import global_ as global__cls
class export_boundary_mesh(Command):
    """
    Export boundary mesh file.
    
    Parameters
    ----------
        filename_2 : str
            Output file name.
        boundary_list : typing.List[str]
            Select boundary zones for exporting mesh.
        global_ : bool
            Enable/disable output of mesh global number.
    
    """

    fluent_name = "export-boundary-mesh"

    argument_names = \
        ['filename', 'boundary_list', 'global_']

    _child_classes = dict(
        filename=filename_2_cls,
        boundary_list=boundary_list_cls,
        global_=global__cls,
    )

