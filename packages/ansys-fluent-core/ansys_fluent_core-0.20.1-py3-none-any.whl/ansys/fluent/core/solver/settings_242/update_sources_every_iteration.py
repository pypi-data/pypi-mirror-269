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

class update_sources_every_iteration(Boolean):
    """
    Enable/disable update of DPM sources in the flow equations at every flow solver iteration. For unsteady simulations, this option is default and recommended.
    """

    fluent_name = "update-sources-every-iteration?"

