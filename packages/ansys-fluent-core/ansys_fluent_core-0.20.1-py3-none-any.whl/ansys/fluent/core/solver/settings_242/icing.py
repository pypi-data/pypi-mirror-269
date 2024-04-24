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

from .fensapice_flow_bc_subtype import fensapice_flow_bc_subtype as fensapice_flow_bc_subtype_cls
from .fensapice_dpm_rh_mode import fensapice_dpm_rh_mode as fensapice_dpm_rh_mode_cls
from .fensapice_drop_vrh import fensapice_drop_vrh as fensapice_drop_vrh_cls
from .fensapice_drop_vc import fensapice_drop_vc as fensapice_drop_vc_cls
class icing(Group):
    """
    Help not available.
    """

    fluent_name = "icing"

    child_names = \
        ['fensapice_flow_bc_subtype', 'fensapice_dpm_rh_mode',
         'fensapice_drop_vrh', 'fensapice_drop_vc']

    _child_classes = dict(
        fensapice_flow_bc_subtype=fensapice_flow_bc_subtype_cls,
        fensapice_dpm_rh_mode=fensapice_dpm_rh_mode_cls,
        fensapice_drop_vrh=fensapice_drop_vrh_cls,
        fensapice_drop_vc=fensapice_drop_vc_cls,
    )

