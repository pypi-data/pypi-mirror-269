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

from .theta import theta as theta_cls
from .coll_dphi import coll_dphi as coll_dphi_cls
class beam_width(Group):
    """
    Beam width settings.
    """

    fluent_name = "beam-width"

    child_names = \
        ['theta', 'coll_dphi']

    _child_classes = dict(
        theta=theta_cls,
        coll_dphi=coll_dphi_cls,
    )

    _child_aliases = dict(
        coll_dtheta="theta",
    )

