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

class enabled(Boolean, _HasAllowedValuesMixin):
    """
    Specify whether the injection's particles are accounted for in terms of volume displacement (DDPM).
    """

    fluent_name = "enabled?"

