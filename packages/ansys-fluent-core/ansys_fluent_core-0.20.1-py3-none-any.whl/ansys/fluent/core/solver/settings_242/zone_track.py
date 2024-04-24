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

from .track_zone import track_zone as track_zone_cls
class zone_track(Group):
    """
    Allows you to attach the reference frame to a zone. You can specify reference frame location and orientation.
    """

    fluent_name = "zone-track"

    child_names = \
        ['track_zone']

    _child_classes = dict(
        track_zone=track_zone_cls,
    )

