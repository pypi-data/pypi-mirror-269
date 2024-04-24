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

from .backflow_total_temperature import backflow_total_temperature as backflow_total_temperature_cls
class thermal(Group):
    """
    Help not available.
    """

    fluent_name = "thermal"

    child_names = \
        ['backflow_total_temperature']

    _child_classes = dict(
        backflow_total_temperature=backflow_total_temperature_cls,
    )

    _child_aliases = dict(
        t0="backflow_total_temperature",
    )

