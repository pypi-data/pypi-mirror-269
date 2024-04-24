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

from .across_injections_enabled import across_injections_enabled as across_injections_enabled_cls
from .min_parcel_count import min_parcel_count as min_parcel_count_cls
class data_reduction(Group):
    """
    Combines groups of DPM parcels that are similar in all relevant aspects into one new parcel each.
    """

    fluent_name = "data-reduction"

    child_names = \
        ['across_injections_enabled', 'min_parcel_count']

    _child_classes = dict(
        across_injections_enabled=across_injections_enabled_cls,
        min_parcel_count=min_parcel_count_cls,
    )

