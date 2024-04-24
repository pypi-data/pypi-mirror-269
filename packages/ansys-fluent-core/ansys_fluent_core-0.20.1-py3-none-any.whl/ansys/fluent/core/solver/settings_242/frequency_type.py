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

class frequency_type(String, _HasAllowedValuesMixin):
    """
    Set the auto save frequency type. For steady flows you will specify the frequency in iterations, while for unsteady flows you will specify it in either time steps or flow time.
    """

    fluent_name = "frequency-type"

