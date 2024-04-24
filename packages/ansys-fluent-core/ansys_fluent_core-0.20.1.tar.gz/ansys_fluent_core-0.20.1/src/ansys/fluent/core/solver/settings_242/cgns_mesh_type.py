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

class cgns_mesh_type(String, _HasAllowedValuesMixin):
    """
    Allows you to choose whether the mesh is mixed (default), its native format, or polyhedral.
    """

    fluent_name = "cgns-mesh-type"

