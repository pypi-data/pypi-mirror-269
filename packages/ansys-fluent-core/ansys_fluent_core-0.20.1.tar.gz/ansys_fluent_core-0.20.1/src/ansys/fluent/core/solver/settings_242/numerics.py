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

from .tracking_1 import tracking as tracking_cls
from .source_term_settings import source_term_settings as source_term_settings_cls
from .node_based_averaging import node_based_averaging as node_based_averaging_cls
from .dynamic_interaction_range_enabled import dynamic_interaction_range_enabled as dynamic_interaction_range_enabled_cls
from .parcel_count_control import parcel_count_control as parcel_count_control_cls
from .high_res_tracking import high_res_tracking as high_res_tracking_cls
class numerics(Group):
    """
    Main menu to allow users to set options controlling the solution of ordinary differential equations describing 
    the underlying physics of the Discrete Phase Model.
    For more details consult the help option of the corresponding menu or TUI command.
    """

    fluent_name = "numerics"

    child_names = \
        ['tracking', 'source_term_settings', 'node_based_averaging',
         'dynamic_interaction_range_enabled', 'parcel_count_control',
         'high_res_tracking']

    _child_classes = dict(
        tracking=tracking_cls,
        source_term_settings=source_term_settings_cls,
        node_based_averaging=node_based_averaging_cls,
        dynamic_interaction_range_enabled=dynamic_interaction_range_enabled_cls,
        parcel_count_control=parcel_count_control_cls,
        high_res_tracking=high_res_tracking_cls,
    )

    _child_aliases = dict(
        averaging="node_based_averaging",
        source_terms="source_term_settings",
    )

