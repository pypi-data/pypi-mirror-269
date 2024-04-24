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

from .bounded_zones import bounded_zones as bounded_zones_cls
from .comfortable_region import comfortable_region as comfortable_region_cls
from .automatic_coordinate import automatic_coordinate as automatic_coordinate_cls
class get_bounds(Command):
    """
    Get bounds based on selects zones.
    
    Parameters
    ----------
        bounded_zones : typing.List[str]
            Zones used to determine region bounds.
        comfortable_region : bool
            Use comfortable region than the selected zones.
        automatic_coordinate : bool
            Update the cylindrical coordinate system automatically.
    
    """

    fluent_name = "get-bounds"

    argument_names = \
        ['bounded_zones', 'comfortable_region', 'automatic_coordinate']

    _child_classes = dict(
        bounded_zones=bounded_zones_cls,
        comfortable_region=comfortable_region_cls,
        automatic_coordinate=automatic_coordinate_cls,
    )

