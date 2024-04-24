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

from .smoothing_1 import smoothing as smoothing_cls
from .remeshing import remeshing as remeshing_cls
class post_morph(Group):
    """
    Mesh quality settings.
    """

    fluent_name = "post-morph"

    child_names = \
        ['smoothing', 'remeshing']

    _child_classes = dict(
        smoothing=smoothing_cls,
        remeshing=remeshing_cls,
    )

