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

class mask_shape_sensitivity(Boolean):
    """
    When enabled, this option will mask the shape sensitivity along the fixed surfaces to reduce the freeform deformation. This improves the deformation smoothness by reducing the need for correction during the secondary morphing.
    """

    fluent_name = "mask-shape-sensitivity"

