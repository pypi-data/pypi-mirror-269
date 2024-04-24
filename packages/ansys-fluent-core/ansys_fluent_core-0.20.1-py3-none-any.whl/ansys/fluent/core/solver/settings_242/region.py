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

from .modifiable_zones import modifiable_zones as modifiable_zones_cls
from .region_type import region_type as region_type_cls
from .show_bounding_region import show_bounding_region as show_bounding_region_cls
from .auto_display import auto_display as auto_display_cls
from .cartesian import cartesian as cartesian_cls
from .cylindrical import cylindrical as cylindrical_cls
from .get_bounds import get_bounds as get_bounds_cls
from .larger_region import larger_region as larger_region_cls
from .smaller_region import smaller_region as smaller_region_cls
class region(Group):
    """
    Design tool region menu.
    """

    fluent_name = "region"

    child_names = \
        ['modifiable_zones', 'region_type', 'show_bounding_region',
         'auto_display', 'cartesian', 'cylindrical']

    command_names = \
        ['get_bounds', 'larger_region', 'smaller_region']

    _child_classes = dict(
        modifiable_zones=modifiable_zones_cls,
        region_type=region_type_cls,
        show_bounding_region=show_bounding_region_cls,
        auto_display=auto_display_cls,
        cartesian=cartesian_cls,
        cylindrical=cylindrical_cls,
        get_bounds=get_bounds_cls,
        larger_region=larger_region_cls,
        smaller_region=smaller_region_cls,
    )

