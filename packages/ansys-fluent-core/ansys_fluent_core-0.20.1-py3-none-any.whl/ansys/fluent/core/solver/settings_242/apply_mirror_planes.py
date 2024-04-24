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

from .mirror_planes_1 import mirror_planes as mirror_planes_cls
class apply_mirror_planes(Command):
    """
    To apply mirror planes for a symmetric or non-symmetric domain.
    
    Parameters
    ----------
        mirror_planes : typing.List[str]
            To apply selectd mirror planes.
    
    """

    fluent_name = "apply-mirror-planes"

    argument_names = \
        ['mirror_planes']

    _child_classes = dict(
        mirror_planes=mirror_planes_cls,
    )

