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

from .criteria import criteria as criteria_cls
from .post_morph import post_morph as post_morph_cls
class mesh_quality(Group):
    """
    Mesh quality settings.
    """

    fluent_name = "mesh-quality"

    child_names = \
        ['criteria', 'post_morph']

    _child_classes = dict(
        criteria=criteria_cls,
        post_morph=post_morph_cls,
    )

